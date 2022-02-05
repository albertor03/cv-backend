from bson import ObjectId

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response

from .serializers import (
    EducationSerializer,
    CreateEducationSerializer,
    EducationModels
)


class ListCreateEducationAPIView(generics.ListCreateAPIView):
    serializer_class = CreateEducationSerializer
    list_serializer_class = EducationSerializer
    statusCode = status.HTTP_400_BAD_REQUEST

    def get(self, request, **kwargs):
        data = {'data': {}, 'errors': []}
        education = self.get_serializer().Meta.model.objects.all()
        education_serializer = self.list_serializer_class(education, many=True, context={'request': request})

        data['data'] = education_serializer.data
        data['errors'].clear()
        data['total_user'] = len(education_serializer.data)
        self.statusCode = status.HTTP_200_OK
        return Response(data, status=self.statusCode)

    def post(self, request, *args, **kwargs):
        data = {'data': {}, 'errors': []}

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            education = serializer.save()
            data['data'] = self.list_serializer_class(education, context={'request': request}).data
            data['errors'].clear()
            self.statusCode = status.HTTP_201_CREATED

        return Response(data, self.statusCode)


class RetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        queryset = EducationModels.objects.filter(_id=ObjectId(self.kwargs["pk"])).first()
        return queryset

    serializer_class = CreateEducationSerializer
    list_serializer_class = EducationSerializer
    statusCode = status.HTTP_400_BAD_REQUEST

    def get(self, request, **kwargs):
        education = self.get_queryset()
        data = {'data': {}, 'errors': ['Information not found.']}
        self.statusCode = status.HTTP_404_NOT_FOUND

        if education:
            education_serializer = self.list_serializer_class(education, context={'request': request})
            data["data"] = education_serializer.data
            data["errors"].clear()
            self.statusCode = status.HTTP_200_OK

        return Response(data, status=self.statusCode)

    def put(self, request, **kwargs):
        education = self.get_queryset()
        data = {'data': {}, 'errors': ['Information not found.']}
        self.statusCode = status.HTTP_404_NOT_FOUND

        if education:
            serializer = self.list_serializer_class(education, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                data["data"] = serializer.data
                data["errors"].clear()
                self.statusCode = status.HTTP_200_OK

        return Response(data, status=self.statusCode)

    def patch(self, request, **kwargs):
        education = self.get_queryset()
        data = {'data': {}, 'errors': ['Information not found.']}
        if education:
            serializer = self.list_serializer_class(education, request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                data["data"] = serializer.data
                data["errors"].clear()
                self.statusCode = status.HTTP_200_OK

        return Response(data, status=self.statusCode)

    def delete(self, request, **kwargs):
        education = self.get_queryset()
        data = {'data': {}, 'errors': ['Information not found.']}
        self.statusCode = status.HTTP_404_NOT_FOUND
        if education:
            education.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(data, status=self.statusCode)

