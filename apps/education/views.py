from bson import ObjectId

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response

from .serializers import (
    EducationSerializer,
    CreateEducationSerializer,
    EducationModels
)
from ..Utilities.utilities import Utilities


class ListCreateEducationAPIView(generics.ListCreateAPIView):
    serializer_class = CreateEducationSerializer
    list_serializer_class = EducationSerializer
    data, statusCode = Utilities.bad_responses('bad_request')

    def get(self, request, **kwargs):
        serializer = self.list_serializer_class(self.get_serializer().Meta.model.objects.all(),
                                                many=True, context={'request': request})
        if serializer:
            self.data, self.statusCode = Utilities.ok_response('ok', serializer.data)
            self.data['total_educations'] = len(serializer.data)

        return Response(self.data, status=self.statusCode)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if self.data.get('total_educations', False):
            self.data.pop("total_educations")

        if serializer.is_valid():
            education = serializer.save()
            self.data, self.statusCode = Utilities.ok_response(
                'post', self.list_serializer_class(education, context={'request': request}).data)

        return Response(self.data, self.statusCode)


class RetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        queryset = EducationModels.objects.filter(_id=ObjectId(self.kwargs["pk"])).first()
        return queryset

    serializer_class = CreateEducationSerializer
    list_serializer_class = EducationSerializer
    data, statusCode = Utilities.bad_responses('bad_request')

    def get(self, request, **kwargs):
        education = self.get_queryset()
        self.data, self.statusCode = Utilities.bad_responses('not_found')

        if education:
            self.data, self.statusCode = Utilities.ok_response(
                'ok', self.list_serializer_class(education, context={'request': request}).data)

        return Response(self.data, status=self.statusCode)

    def put(self, request, **kwargs):
        education = self.get_queryset()
        self.data, self.statusCode = Utilities.bad_responses('not_found')

        if education:
            serializer = self.list_serializer_class(education, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                self.data, self.statusCode = Utilities.ok_response('ok', serializer.data)

        return Response(self.data, status=self.statusCode)

    def patch(self, request, **kwargs):
        education = self.get_queryset()
        self.data, self.statusCode = Utilities.bad_responses('not_found')
        if education:
            serializer = self.list_serializer_class(education, request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                self.data, self.statusCode = Utilities.ok_response('ok', serializer.data)

        return Response(self.data, status=self.statusCode)

    def delete(self, request, **kwargs):
        education = self.get_queryset()
        self.data, self.statusCode = Utilities.bad_responses('not_found')
        if education:
            education.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(self.data, status=self.statusCode)
