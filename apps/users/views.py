import jwt

from bson import ObjectId
from chance import chance

from django.utils import timezone
from django.conf import settings
from django.contrib.auth import authenticate

from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.exceptions import NotFound

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import (
    UserRegisterSerializer,
    UserSerializer,
    RestorePasswordSerializer, SendActiveLinkUserSerializer, SendResetPwdLinkUserSerializer, UserDetailSerializer,
)

from ..send_email.email import SendEmail
from ..Utilities.utilities import Utilities


class SingUpUserApiView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    data, statusCode = Utilities.bad_responses('bad_request')
    permission_classes = [AllowAny]

    def post(self, request, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            req = {'username': request.data['username'], 'password': request.data['password']}
            user = serializer.save()
            user.is_active = True
            user.save()
            data = MakeToken().create_token(req)
            user.is_active = False
            user.save()

            url = reverse('active_user', kwargs={'token': data['token']}, request=request)

            self.data['errors'] = [SendEmail().send_simple_message(user.email, "User Register",
                                                                   f"User register body {url}")]

            if not self.data['errors'][0]:
                self.data, self.statusCode = Utilities.ok_response('post', UserSerializer(user).data)
            else:
                user.delete()
                self.statusCode = status.HTTP_424_FAILED_DEPENDENCY

        return Response(self.data, status=self.statusCode)


class AllUserApiView(generics.ListAPIView):
    serializer_class = UserSerializer
    data, statusCode = Utilities.bad_responses('bad_request')

    def get(self, request, **kwargs):
        serializer = self.serializer_class(self.get_serializer().Meta.model.objects.all(), many=True,
                                           context={'request': request}).data
        self.data, self.statusCode = Utilities.ok_response(serializer=serializer)
        self.data['total_users'] = len(serializer)

        return Response(self.data, status=self.statusCode)


class DetailUserApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer
    queryset = serializer_class.Meta.model.objects.all()
    data, statusCode = Utilities.bad_responses()

    def get_queryset(self, *args, **kwargs):
        queryset = self.serializer_class.Meta.model.objects.filter(_id=ObjectId(self.kwargs['pk'])).first()
        if not queryset:
            raise NotFound({'data': {}, 'errors': ['User not exist.']})
        return queryset

    def get(self, request, pk=None, **kwargs):
        user = self.get_queryset()
        self.data, self.statusCode = Utilities.ok_response('ok', self.serializer_class(
            user, context={'request': request}).data)

        return Response(self.data, status=self.statusCode)

    def put(self, request, pk=None, **kwargs):
        serializer = UserSerializer(self.get_queryset(), request.data)
        if serializer.is_valid():
            serializer.save()
            self.data, self.statusCode = Utilities.ok_response(serializer=serializer.data)

        return Response(self.data, status=self.statusCode)

    def patch(self, request, pk=None, **kwargs):
        serializer = UserSerializer(self.get_queryset(), request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            self.data, self.statusCode = Utilities.ok_response(serializer=serializer.data)

        return Response(self.data, status=self.statusCode)

    def delete(self, request, pk=None, **kwargs):
        self.get_queryset().delete()
        self.data, self.statusCode = Utilities.ok_response('patch')

        return Response(self.data, self.statusCode)


class LoginAPIView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    data, statusCode = Utilities.bad_responses()

    def post(self, request, *args, **kwargs):
        self.data = {'data': {}, 'errors': ['Invalid credentials.']}
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(
            username=username,
            password=password
        )
        if user:
            if not user.is_active:
                self.data['errors'] = ['Inactive user.']
                self.statusCode = status.HTTP_403_FORBIDDEN
            else:
                data = MakeToken().create_token(request.data)
                if data:
                    self.data, self.statusCode = Utilities.ok_response(serializer=data)
                    user.last_login = timezone.now()
                    user.save()
        else:
            self.data['data'] = {}

        return Response(self.data, status=self.statusCode)


class LogoutAPIView(APIView):
    data = {'data': 'Successfully logged out.', 'errors': []}
    statusCode = status.HTTP_200_OK

    def get(self, request):
        token = request.headers['Authorization'].split()[1]
        decode_token = DecodeToken().decode_token(token)
        user = User.objects.filter(_id=ObjectId(decode_token['user_id'])).first()
        if user:
            RefreshToken.for_user(user)

        return Response(self.data, status=self.statusCode)


class ResetPasswordOfLoggedInUserAPIView(generics.GenericAPIView):
    serializer_class = RestorePasswordSerializer
    data = {'data': '', 'errors': ['Invalid request.']}
    statusCode = status.HTTP_400_BAD_REQUEST

    def patch(self, request, *args, **kwargs):
        token = request.headers['Authorization'].split()[1]
        decode_token = DecodeToken().decode_token(token)
        request.data['user_id'] = decode_token['user_id']
        user = User.objects.filter(_id=ObjectId(decode_token['user_id'])).first()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.update(user, serializer.validated_data)
            self.data['data'] = 'Password updated successfully.'
            self.data['errors'].clear()
            self.statusCode = status.HTTP_200_OK

        return Response(self.data, status=self.statusCode)


class ActiveUserAPIView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, pk=None, *args, **kwargs):
        decode_token = DecodeToken().decode_token(kwargs['token'])
        data = {'data': str(), 'errors': ['Bad request.']}
        status_code = status.HTTP_400_BAD_REQUEST

        user = User.objects.filter(_id=ObjectId(decode_token['user_id']))
        if user.exists():
            if user.first().is_active:
                data['data'] = ""
                data['errors'] = ['The user is already activated.']
            else:
                user = user.first()
                user.is_active = True
                user.save()
                data['data'] = 'User active successfully.'
                data['errors'].clear()
                status_code = status.HTTP_200_OK

        return Response(data, status=status_code)


class SendActivateLinkAPIView(generics.CreateAPIView):
    serializer_class = SendActiveLinkUserSerializer
    data = {'data': '', 'errors': ['Bad request.']}
    statusCode = status.HTTP_400_BAD_REQUEST

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            user.is_active = False
            user.save()
            data = RefreshToken.for_user(user).access_token
            user.is_active = False
            user.save()
            url = reverse('active_user', kwargs={'token': data}, request=request)
            resp = SendEmail().send_simple_message(user.email, "User activation", f"User register body {url}")
            if not resp:
                self.data['data'] = 'User activation link sent successfully.'
                self.data['errors'].clear()
                self.statusCode = status.HTTP_200_OK
            else:
                self.data['data'] = ''
                self.data['errors'] = ["Something happened while sending the user activate email."]
                self.statusCode = status.HTTP_424_FAILED_DEPENDENCY

        return Response(self.data, status=self.statusCode)


class SendResetPasswordLinkAPIView(generics.GenericAPIView):
    serializer_class = SendResetPwdLinkUserSerializer
    data = {'data': '', 'errors': ['Bad request.']}
    statusCode = status.HTTP_400_BAD_REQUEST

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_pwd = chance.string(length=8)
            user = serializer.validated_data
            user.set_password(new_pwd)
            user.save()
            data = RefreshToken.for_user(user).access_token
            url = reverse('reset_password_of_user_logged', request=request)
            resp = SendEmail().send_simple_message(user.email, "Reset password", f"The password was changed, "
                                                                                 f"please enter in the url {url} with "
                                                                                 f"the new password {new_pwd} to "
                                                                                 f"change your password. JWT {data} ")

            if not resp:
                self.data['data'] = 'Reset password link sent successfully.'
                self.data['errors'].clear()
                self.statusCode = status.HTTP_200_OK
            else:
                self.data['data'] = ''
                self.data['errors'] = ["Something happened while sending the user activate email."]
                self.statusCode = status.HTTP_424_FAILED_DEPENDENCY

        return Response(self.data, status=self.statusCode)


class DecodeToken:

    @staticmethod
    def decode_token(token):
        return jwt.decode(token, settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=[settings.SIMPLE_JWT['ALGORITHM']],)


class MakeToken:
    data = {}

    def create_token(self, request):
        login = TokenObtainPairSerializer(data=request)
        if login.is_valid():
            decode_token = DecodeToken().decode_token(login.validated_data['access'])
            self.data = {'token': login.validated_data['access'], 'refresh': login.validated_data['refresh'],
                         'exp': decode_token['exp']}

        return self.data
