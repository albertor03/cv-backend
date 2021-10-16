from bson import ObjectId

from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.users.serializers import UserSerializer, User, UserRegisterSerializer, UserUpdateSerializer


class UserViewSet(viewsets.GenericViewSet):
    model = User
    serializer_class = UserSerializer

    response = {'data': '', 'error': []}
    statusCode = status.HTTP_200_OK

    def get_object(self, pk):
        return self.model.objects.filter(_id=ObjectId(pk), is_active__in=[True]).values(
                '_id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'last_login', 'created_at',
                'updated_at').first()

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.filter(is_active__in=[True]).values(
                '_id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'last_login', 'created_at',
                'updated_at'
            )
        return self.queryset

    def list(self, request):
        users = self.get_queryset()
        users_serializer = self.serializer_class(users, many=True)
        self.response['data'] = users_serializer.data
        return Response(self.response)

    def create(self, request):
        user_serializer = UserRegisterSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            self.response['data'] = request.data
            self.statusCode = status.HTTP_201_CREATED
        else:
            self.response['data'] = ''
            self.response['error'] = user_serializer.errors
            self.statusCode = status.HTTP_400_BAD_REQUEST

        return Response(self.response, status=self.statusCode)

    def retrieve(self, request, pk=None):
        user = self.get_object(pk)
        if user is not None:
            user_serializer = self.serializer_class(user)
            self.response['data'] = user_serializer.data
            self.response['error'] = []
        else:
            self.response['data'] = ''
            self.response['error'] = ['User not found.']
            self.statusCode = status.HTTP_400_BAD_REQUEST

        return Response(self.response, status=self.statusCode)

    def update(self, request, pk):
        user = self.model.objects.filter(_id=ObjectId(pk), is_active__in=[True]).first()
        if user:
            user_serializer = UserUpdateSerializer(user, data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                self.response['data'] = user_serializer.data
                self.response['error'] = user_serializer.errors
        else:
            self.response['data'] = ''
            self.response['error'] = ['User not found.']
            self.statusCode = status.HTTP_400_BAD_REQUEST

        return Response(self.response, status=self.statusCode)

    def destroy(self, request, pk=None):
        user_destroy = self.model.objects.filter(_id=ObjectId(pk)).update(is_active=False)
        if user_destroy == 1:
            self.response['data'] = 'User deleted.'
            self.response['error'] = []
        else:
            self.response['data'] = ''
            self.response['error'] = ['User not found.']
            self.statusCode = status.HTTP_400_BAD_REQUEST

        return Response(self.response, status=self.statusCode)
