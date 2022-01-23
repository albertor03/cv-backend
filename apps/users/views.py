import jwt

from bson import ObjectId

from django.contrib.auth import authenticate
from django.urls import reverse_lazy
from django.utils import timezone
from django.conf import settings

from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import (
    UserRegisterSerializer,
    UserSerializer,
    RestorePasswordSerializer,
)

from ..send_email.email import SendEmail


class SingUpUserApiView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    data = {}
    statusCode = status.HTTP_400_BAD_REQUEST
    permission_classes = [AllowAny]

    def post(self, request, **kwargs):
        self.data = {'data': {}, 'errors': ['Bad request.']}
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            req = {'username': request.data['username'], 'password': request.data['password']}
            user = serializer.save()
            user.is_active = True
            user.save()
            data = MakeToken().create_token(req)
            user.is_active = False
            user.save()

            resp = SendEmail().send_simple_message("alberto.zapata.orta@gmail.com", "User Register",
                                                   f"User register body "
                                                   f"{reverse_lazy('active_user', kwargs={'pk': data['token']})}")

            if resp.status_code == status.HTTP_200_OK:
                self.data['data'] = UserSerializer(user).data
                self.data['errors'] = []
                self.statusCode = status.HTTP_201_CREATED
            else:
                user.delete()
                self.data['errors'] = ["Something happened while sending the user registration email."]
                self.statusCode = status.HTTP_424_FAILED_DEPENDENCY

        return Response(self.data, status=self.statusCode)


class AllUserApiView(generics.ListAPIView):
    data = {}
    error = []
    statusCode = status.HTTP_200_OK

    def get(self, request, **kwargs):
        user = User.objects.all()
        users_serializer = UserSerializer(user, many=True)

        self.data['data'] = users_serializer.data
        self.data['errors'] = self.error
        self.data['total_user'] = len(users_serializer.data)

        return Response(self.data, status=self.statusCode)


class DetailUserApiView(APIView):
    serializer_class = UserSerializer
    data = {}
    error = []
    statusCode = status.HTTP_200_OK

    @staticmethod
    def get_object(pk=None):
        return User.objects.filter(_id=ObjectId(pk)).first()

    def get(self, request, pk=None):
        user = self.get_object(pk)
        user_data = {}
        self.error = ['User not found.']
        self.statusCode = status.HTTP_404_NOT_FOUND

        if user:
            user_serializer = UserSerializer(user)
            user_data = user_serializer.data
            self.error = []
            self.statusCode = status.HTTP_200_OK

        self.data["data"] = user_data
        self.data["errors"] = self.error

        return Response(self.data, status=self.statusCode)

    def put(self, request, pk):
        user = self.get_object(pk)
        self.error = ['User not found.']
        if user:
            serializer = UserSerializer(user, request.data)
            if serializer.is_valid():
                serializer.save()
                self.data["data"] = serializer.data
                self.data["errors"] = []

        return Response(self.data, status=self.statusCode)

    def patch(self, request, pk):
        user = self.get_object(pk)
        self.error = ['User not found.']
        if user:
            serializer = UserSerializer(user, request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                self.data["data"] = serializer.data
                self.data["errors"] = []

        return Response(self.data, status=self.statusCode)

    def delete(self, request, pk):
        user = self.get_object(pk)
        if user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(self.data, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    data = {}
    statusCode = status.HTTP_400_BAD_REQUEST

    def post(self, request, *args, **kwargs):
        self.data = {'data': dict(), 'errors': ['Invalid credentials.']}
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
                    self.data['data'] = data
                    self.data['errors'].clear()
                    self.statusCode = status.HTTP_200_OK
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
        else:
            self.data['data'] = ''
            self.data['errors'] = ['Invalid token.']
            self.statusCode = status.HTTP_400_BAD_REQUEST

        return Response(self.data, status=self.statusCode)


class ResetPasswordOfLoggedInUserAPIView(generics.UpdateAPIView):
    serializer_class = RestorePasswordSerializer
    data = {'data': '', 'errors': ['Invalid request.']}
    statusCode = status.HTTP_400_BAD_REQUEST

    def patch(self, request, *args, **kwargs):
        token = request.headers['Authorization'].split()[1]
        decode_token = DecodeToken().decode_token(token)
        try:
            request.data._mutable = True
            request.data['user_id'] = decode_token['user_id']
            request.data._mutable = False
        except AttributeError as e:
            str(e)
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
    data = {'data': str(), 'errors': ['Bad request.']}
    statusCode = status.HTTP_400_BAD_REQUEST
    permission_classes = [AllowAny]

    def patch(self, request, pk=None, *args, **kwargs):
        decode_token = DecodeToken().decode_token(pk)

        user = User.objects.filter(_id=ObjectId(decode_token['user_id']))
        if user.exists():
            if user.first().is_active:
                self.data['data'] = ""
                self.data['errors'] = ['The user is already activated.']
            else:
                user = user.first()
                user.is_active = True
                user.save()
                self.data['data'] = 'User active successfully.'
                self.data['errors'].clear()
                self.statusCode = status.HTTP_200_OK

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
