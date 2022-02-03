from bson import ObjectId

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response

from .serializers import (
    CreateJobSerializer,
    ListJobSerializer,
    JobModels
)


class ListCreateJobAPIView(generics.ListCreateAPIView):
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

    def get_queryset(self):
        queryset = JobModels.objects.filter(_id=ObjectId(self.kwargs['pk'])).first()
        return queryset

    serializer_class = CreateJobSerializer
    list_serializer_class = ListJobSerializer
    data = {'data': {}, 'errors': []}
    statusCode = status.HTTP_400_BAD_REQUEST

    def get(self, request, **kwargs):
        info = self.get_queryset()
        self.data = {'data': {}, 'errors': ['Job not found.']}
        self.statusCode = status.HTTP_404_NOT_FOUND

        if info:
            info_serializer = self.list_serializer_class(info)
            self.data["data"] = info_serializer.data
            self.data["errors"] = []
            self.statusCode = status.HTTP_200_OK

        return Response(self.data, status=self.statusCode)

    def put(self, request, **kwargs):
        info = self.get_queryset()
        self.data = {'data': {}, 'errors': ['Information not found.']}
        self.statusCode = status.HTTP_404_NOT_FOUND

        if info:
            serializer = self.list_serializer_class(info, data=request.data)
            if serializer.is_valid():
                serializer.save()
                self.data["data"] = serializer.data
                self.data["errors"] = []
                self.statusCode = status.HTTP_200_OK

        return Response(self.data, status=self.statusCode)

    def patch(self, request, **kwargs):
        user = self.get_queryset()
        self.data = {'data': {}, 'errors': ['Information not found.']}
        if user:
            serializer = self.list_serializer_class(user, request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                self.data["data"] = serializer.data
                self.data["errors"].clear()
                self.statusCode = status.HTTP_200_OK

        return Response(self.data, status=self.statusCode)

    def delete(self, request, **kwargs):
        user = self.get_queryset()
        self.data = {'data': {}, 'errors': ['Information not found.']}
        self.statusCode = status.HTTP_404_NOT_FOUND
        if user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(self.data, status=self.statusCode)
