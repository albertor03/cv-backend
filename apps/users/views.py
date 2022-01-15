from bson import ObjectId
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView

from .models import User
from .serializers import UserRegisterSerializer, UserSerializer


class SingUpUserApiView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    data = {}
    statusCode = status.HTTP_400_BAD_REQUEST

    def post(self, request, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self.data['data'] = UserSerializer(user).data
        self.data['errors'] = []
        self.statusCode = status.HTTP_201_CREATED

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
