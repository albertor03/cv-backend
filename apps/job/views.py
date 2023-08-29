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

from ..Utilities.utilities import Utilities


class ListCreateJobAPIView(generics.ListCreateAPIView):
    serializer_class = CreateJobSerializer
    data, statusCode = Utilities.bad_responses('bad_request')

    def get(self, request, **kwargs):
        serializer = ListJobSerializer(JobModels.objects.all(), many=True)

        if serializer:
            self.data, self.statusCode = Utilities.ok_response('ok', serializer.data)
            self.data['total_jobs'] = len(serializer.data)

        return Response(self.data, status=self.statusCode)

    def post(self, request, *args, **kwargs):
        self.data.clear()
        serializer = CreateJobSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            self.data, self.statusCode = Utilities.ok_response('post', serializer.data)

        return Response(self.data, status=self.statusCode)


class RetrieveUpdateDestroyJobAPIView(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        queryset = JobModels.objects.filter(_id=ObjectId(self.kwargs['pk'])).first()
        return queryset

    serializer_class = CreateJobSerializer
    list_serializer_class = ListJobSerializer
    data, statusCode = Utilities.bad_responses('bad_request')

    def get(self, request, **kwargs):
        self.data, self.statusCode = Utilities.bad_responses('not_found')

        if self.get_queryset():
            self.data, self.statusCode = Utilities.ok_response('ok',
                                                               self.list_serializer_class(self.get_queryset()).data)

        return Response(self.data, status=self.statusCode)

    def put(self, request, **kwargs):
        job = self.get_queryset()
        self.data, self.statusCode = Utilities.bad_responses('not_found')

        if job:
            serializer = self.list_serializer_class(job, data=request.data)
            if serializer.is_valid():
                serializer.save()
                self.data, self.statusCode = Utilities.ok_response('ok', serializer.data)

        return Response(self.data, status=self.statusCode)

    def patch(self, request, **kwargs):
        job = self.get_queryset()
        self.data, self.statusCode = Utilities.bad_responses('not_found')
        if job:
            serializer = ActiveJobSerializer(job, request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                self.data, self.statusCode = Utilities.ok_response('ok', serializer.data)

        return Response(self.data, status=self.statusCode)

    def delete(self, request, **kwargs):
        job = self.get_queryset()
        self.data, self.statusCode = Utilities.bad_responses('not_found')
        if job:
            job.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(self.data, status=self.statusCode)
