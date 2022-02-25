from bson import ObjectId

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response

from .serializers import (
    CreateJobSerializer,
    ListJobSerializer,
    JobModels,
    ActiveJobSerializer
)


def _return_not_found_response():
    return {'data': {}, 'errors': ['Information not found.']}, status.HTTP_404_NOT_FOUND


class ListCreateJobAPIView(generics.ListCreateAPIView):
    serializer_class = CreateJobSerializer
    data = {'data': {}, 'errors': ['Bad request.']}
    statusCode = status.HTTP_400_BAD_REQUEST

    def get(self, request, **kwargs):
        job_serializer = ListJobSerializer(JobModels.objects.all(), many=True)
        self.data['errors'].clear()
        self.statusCode = status.HTTP_200_OK

        if job_serializer:
            self.data['data'] = job_serializer.data
            self.data['total_jobs'] = len(job_serializer.data)

        return Response(self.data, status=self.statusCode)

    def post(self, request, *args, **kwargs):
        serializer = CreateJobSerializer(data=request.data)

        if self.data.get('total_user', False):
            self.data.pop("total_user")

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
        self.data, self.statusCode = _return_not_found_response()

        if info:
            info_serializer = self.list_serializer_class(info)
            self.data["data"] = info_serializer.data
            self.data["errors"].clear()
            self.statusCode = status.HTTP_200_OK

        return Response(self.data, status=self.statusCode)

    def put(self, request, **kwargs):
        info = self.get_queryset()
        self.data, self.statusCode = _return_not_found_response()

        if info:
            serializer = self.list_serializer_class(info, data=request.data)
            if serializer.is_valid():
                serializer.save()
                self.data["data"] = serializer.data
                self.data["errors"].clear()
                self.statusCode = status.HTTP_200_OK

        return Response(self.data, status=self.statusCode)

    def patch(self, request, **kwargs):
        user = self.get_queryset()
        self.data, self.statusCode = _return_not_found_response()
        if user:
            serializer = ActiveJobSerializer(user, request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                self.data["data"] = serializer.data
                self.data["errors"].clear()
                self.statusCode = status.HTTP_200_OK

        return Response(self.data, status=self.statusCode)

    def delete(self, request, **kwargs):
        user = self.get_queryset()
        self.data, self.statusCode = _return_not_found_response()
        if user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(self.data, status=self.statusCode)
