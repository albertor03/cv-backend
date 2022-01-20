from bson import ObjectId

from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import (
    CreateJobSerializer,
    ListJobSerializer,
    JobModels
)


class ListCreateJobAPIView(APIView):
    serializer_class = CreateJobSerializer
    data = {'data': {}, 'errors': ['Bad request.']}
    statusCode = status.HTTP_400_BAD_REQUEST

    def get(self, request, **kwargs):
        job = JobModels.objects.all()
        job_serializer = ListJobSerializer(job, many=True)

        self.data['data'] = job_serializer.data
        self.data['errors'].clear()
        self.data['total_user'] = len(job_serializer.data)
        self.statusCode = status.HTTP_200_OK

        return Response(self.data, status=self.statusCode)

    def post(self, request, *args, **kwargs):
        serializer = CreateJobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            self.data['data'] = serializer.data
            self.data['errors'].clear()
            self.statusCode = status.HTTP_201_CREATED

        return Response(self.data, status=self.statusCode)


class RetrieveUpdateDestroyJobAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateJobSerializer
    data = {'data': {}, 'errors': []}
    statusCode = status.HTTP_400_BAD_REQUEST

    @staticmethod
    def get_object(pk=None):
        return JobModels.objects.filter(_id=ObjectId(pk)).first()

    def get(self, request, pk=None, **kwargs):
        info = self.get_object(pk)
        self.data = {'data': {}, 'errors': ['Job not found.']}
        self.statusCode = status.HTTP_404_NOT_FOUND

        if info:
            info_serializer = ListJobSerializer(info)
            self.data["data"] = info_serializer.data
            self.data["errors"] = []
            self.statusCode = status.HTTP_200_OK

        return Response(self.data, status=self.statusCode)

    def put(self, request, pk=None, **kwargs):
        info = self.get_object(pk)
        self.data = {'data': {}, 'errors': ['Information not found.']}
        self.statusCode = status.HTTP_404_NOT_FOUND

        if info:
            serializer = ListJobSerializer(info, data=request.data)
            if serializer.is_valid():
                serializer.save()
                self.data["data"] = serializer.data
                self.data["errors"] = []
                self.statusCode = status.HTTP_200_OK

        return Response(self.data, status=self.statusCode)

    def patch(self, request, pk=None, **kwargs):
        user = self.get_object(pk)
        self.data = {'data': {}, 'errors': ['Information not found.']}
        if user:
            serializer = ListJobSerializer(user, request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                self.data["data"] = serializer.data
                self.data["errors"].clear()
                self.statusCode = status.HTTP_200_OK

        return Response(self.data, status=self.statusCode)

    def delete(self, request, pk=None, **kwargs):
        user = self.get_object(pk)
        self.data = {'data': {}, 'errors': ['Information not found.']}
        self.statusCode = status.HTTP_404_NOT_FOUND
        if user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(self.data, status=self.statusCode)
