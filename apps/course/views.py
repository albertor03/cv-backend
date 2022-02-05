from bson import ObjectId

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response


from .serializers import (
    CourseSectionSerializer,
    CreateCourseSerializer,
    ListCourseSerializer
)


class ListCreateCourseSectionAPIView(generics.ListCreateAPIView):
    serializer_class = CourseSectionSerializer
    data = {'data': {}, 'errors': ['Information not found.']}
    statusCode = status.HTTP_400_BAD_REQUEST

    def get(self, request, *args, **kwargs):
        data = self.get_serializer().Meta.model.objects.all()
        if data:
            serializer = self.serializer_class(data, many=True)
            self.data['data'] = serializer.data
            self.data['errors'].clear()
            self.statusCode = status.HTTP_200_OK

        return Response(self.data, self.statusCode)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            self.data['data'] = serializer.data
            self.data['errors'].clear()
            self.statusCode = status.HTTP_201_CREATED

        return Response(self.data, self.statusCode)


class RetrieveUpdateDestroyCourseSectionAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSectionSerializer
    data = {'data': {}, 'errors': ['Information not found.']}
    statusCode = status.HTTP_400_BAD_REQUEST
    http_method_names = ['get', 'delete', 'patch']

    def get_queryset(self):
        queryset = self.get_serializer().Meta.model.objects.filter(_id=ObjectId(self.kwargs["pk"])).first()
        return queryset

    def get(self, request, *args, **kwargs):
        data = self.get_queryset()
        if data:
            serializer = self.serializer_class(data, context={'request': request})
            self.data["data"] = serializer.data
            self.data["errors"].clear()
            self.statusCode = status.HTTP_200_OK

        return Response(self.data, status=self.statusCode)

    def put(self, request, *args, **kwargs):
        data = self.get_queryset()
        self.statusCode = status.HTTP_404_NOT_FOUND
        if data:
            serializer = self.serializer_class(data, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                self.data["data"] = serializer.data
                self.data["errors"].clear()
                self.statusCode = status.HTTP_200_OK

        return Response(self.data, self.statusCode)

    def patch(self, request, **kwargs):
        data = self.get_queryset()
        if data:
            serializer = self.serializer_class(data, request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                self.data["data"] = serializer.data
                self.data["errors"].clear()
                self.statusCode = status.HTTP_200_OK

        return Response(self.data, status=self.statusCode)

    def delete(self, request, **kwargs):
        data = self.get_queryset()
        self.statusCode = status.HTTP_404_NOT_FOUND
        if data:
            data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(self.data, status=self.statusCode)


class ListCreateCourseAPIView(generics.ListCreateAPIView):
    serializer_class = CreateCourseSerializer
    data = {'data': {}, 'errors': ['Information not found.']}
    statusCode = status.HTTP_400_BAD_REQUEST

    def get(self, request, *args, **kwargs):
        data = self.get_serializer().Meta.model.objects.all()
        self.statusCode = status.HTTP_200_OK
        if data:
            serializer = self.serializer_class(data, many=True)
            self.data['data'] = serializer.data
            self.data['errors'].clear()
        else:
            self.data['data'].clear()
            self.data['errors'].clear()

        return Response(self.data, self.statusCode)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            course = serializer.save()

            self.data['data'] = ListCourseSerializer(course).data
            self.data['errors'].clear()
            self.statusCode = status.HTTP_201_CREATED

        return Response(self.data, self.statusCode)


class RetrieveUpdateDestroyCourseAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateCourseSerializer
    data = {'data': {}, 'errors': ['Information not found.']}
    statusCode = status.HTTP_400_BAD_REQUEST

    def get_queryset(self):
        queryset = self.get_serializer().Meta.model.objects.filter(_id=ObjectId(self.kwargs["pk"])).first()
        return queryset

    def get(self, request, *args, **kwargs):
        data = self.get_queryset()
        if data:
            serializer = self.serializer_class(data, context={'request': request})
            self.data["data"] = serializer.data
            self.data["errors"].clear()
            self.statusCode = status.HTTP_200_OK

        return Response(self.data, status=self.statusCode)

    def put(self, request, *args, **kwargs):
        data = self.get_queryset()
        self.statusCode = status.HTTP_404_NOT_FOUND
        if data:
            serializer = self.serializer_class(data, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                self.data["data"] = serializer.data
                self.data["errors"].clear()
                self.statusCode = status.HTTP_200_OK

        return Response(self.data, self.statusCode)

    def patch(self, request, **kwargs):
        data = self.get_queryset()
        if data:
            serializer = self.serializer_class(data, request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                self.data["data"] = serializer.data
                self.data["errors"].clear()
                self.statusCode = status.HTTP_200_OK

        return Response(self.data, status=self.statusCode)

    def delete(self, request, **kwargs):
        data = self.get_queryset()
        self.statusCode = status.HTTP_404_NOT_FOUND
        if data:
            data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(self.data, status=self.statusCode)