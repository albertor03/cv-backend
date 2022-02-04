from bson import ObjectId

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response


from .serializers import CourseSectionSerializer, CourseSerializer


class ListCreateCourseSectionAPIView(generics.ListCreateAPIView):
    serializer_class = CourseSectionSerializer
    data = {'data': {}, 'errors': ['Information not found.']}
    statusCode = status.HTTP_400_BAD_REQUEST

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            self.data['data'] = serializer.data
            self.data['errors'].clear()
            self.statusCode = status.HTTP_201_CREATED

        return Response(self.data, self.statusCode)


class ListCreateCourseAPIView(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    data = {'data': {}, 'errors': ['Information not found.']}
    statusCode = status.HTTP_400_BAD_REQUEST

    def get(self, request, *args, **kwargs):
        data = self.get_serializer().Meta.model.objects.all()
        serializer = CourseSerializer(data=data, many=True)
        serializer.is_valid()
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


class RetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    data = {'data': {}, 'errors': ['Information not found.']}
    statusCode = status.HTTP_400_BAD_REQUEST

    def get_queryset(self):
        queryset = self.get_serializer().Meta.model.objects.filter(_id=ObjectId(self.kwargs["pk"])).first()
        return queryset

    def get(self, request, *args, **kwargs):
        data = self.get_queryset()
        if data:
            education_serializer = self.serializer_class(data, context={'request': request})
            self.data["data"] = education_serializer.data
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
