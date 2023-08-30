from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response

from .serializers import (
    EducationSerializer
)
from ..Utilities.utilities import Utilities


class ListCreateEducationAPIView(generics.ListCreateAPIView):
    serializer_class = EducationSerializer
    data, statusCode = Utilities.bad_responses('bad_request')

    def get(self, request, **kwargs):
        serializer = self.serializer_class(self.get_serializer().Meta.model.objects.all(),
                                           many=True, context={'request': request})

        self.data, self.statusCode = Utilities.ok_response('ok', serializer.data)
        self.data['total_educations'] = len(serializer.data)

        return Response(self.data, status=self.statusCode)

    def post(self, request, *args, **kwargs):
        self.data.clear()
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            education = serializer.save()
            self.data, self.statusCode = Utilities.ok_response(
                'post', self.serializer_class(education, context={'request': request}).data)

        return Response(self.data, self.statusCode)


class RetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EducationSerializer
    data, statusCode = Utilities.bad_responses('bad_request')

    def get(self, request, **kwargs):
        serializer = self.serializer_class().get_query(self.kwargs["pk"])

        if serializer:
            self.data, self.statusCode = Utilities.ok_response(
                'ok', self.serializer_class(serializer, context={'request': request}).data)

        return Response(self.data, status=self.statusCode)

    def put(self, request, **kwargs):
        data = self.serializer_class().get_query(self.kwargs["pk"])
        serializer = self.serializer_class(data, data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            self.data, self.statusCode = Utilities.ok_response('ok', serializer.data)

        return Response(self.data, status=self.statusCode)

    def patch(self, request, **kwargs):
        data = self.serializer_class().get_query(self.kwargs["pk"])
        serializer = self.serializer_class(data, request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            self.data, self.statusCode = Utilities.ok_response('ok', serializer.data)

        return Response(self.data, status=self.statusCode)

    def delete(self, request, **kwargs):
        data = self.serializer_class().get_query(self.kwargs["pk"])
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
