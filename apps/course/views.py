from bson import ObjectId

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response


from .serializers import (
    UpdateCourseSectionSerializer,
    CreateCourseSerializer,
    CreateCourseSectionSerializer,
    ListUpdateCourseSerializer,
    PatchCourseSerializer,
)
from ..Utilities.utilities import Utilities


class ListCreateCourseSectionAPIView(generics.ListCreateAPIView):
    serializer_class = CreateCourseSectionSerializer
    data, statusCode = Utilities.bad_responses('bad_request')

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_serializer().Meta.model.objects.all(), many=True,
                                           context={'request': request})

        self.data, self.statusCode = Utilities.ok_response(serializer=serializer.data)
        self.data['total_course_sections'] = len(serializer.data)

        return Response(self.data, self.statusCode)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            self.data, self.statusCode = Utilities.ok_response('post', serializer.data)

        return Response(self.data, self.statusCode)


class RetrieveUpdateDestroyCourseSectionAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateCourseSectionSerializer
    update_serializer_class = UpdateCourseSectionSerializer
    data, statusCode = Utilities.bad_responses('bad_request')
    http_method_names = ['patch', 'delete']

    def get_queryset(self):
        queryset = self.get_serializer().Meta.model.objects.filter(_id=ObjectId(self.kwargs["pk"])).first()
        return queryset

    def patch(self, request, *args, **kwargs):
        data = self.get_queryset()
        self.data, self.statusCode = Utilities.bad_responses('not_found')

        if data:
            serializer = self.update_serializer_class(data, request.data, partial=True, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                section = serializer.save()
                self.data, self.statusCode = Utilities.ok_response(serializer=self.serializer_class(section).data)

        return Response(self.data, status=self.statusCode)

    def delete(self, request, **kwargs):
        data = self.get_queryset()
        self.data, self.statusCode = Utilities.bad_responses('not_found')

        if data:
            data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(self.data, status=self.statusCode)


class ListCreateCourseAPIView(generics.ListCreateAPIView):
    serializer_class = CreateCourseSerializer
    list_serializer_class = ListUpdateCourseSerializer
    data, statusCode = Utilities.bad_responses('bad_request')

    def get(self, request, *args, **kwargs):
        serializer = self.list_serializer_class(self.get_serializer().Meta.model.objects.all(), many=True,
                                                context={'request': request})

        self.data, self.statusCode = Utilities.ok_response(serializer=serializer.data)
        self.data['total_courses'] = len(serializer.data)

        return Response(self.data, self.statusCode)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            course = serializer.save()
            self.data, self.statusCode = Utilities.ok_response(
                'post', self.list_serializer_class(course, context={'request': request}).data)

        return Response(self.data, self.statusCode)


class RetrieveUpdateDestroyCourseAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateCourseSerializer
    list_update_serializer_class = ListUpdateCourseSerializer
    path_serializer_class = PatchCourseSerializer
    data, statusCode = Utilities.bad_responses('bad_request')

    def get_queryset(self):
        queryset = self.get_serializer().Meta.model.objects.filter(_id=ObjectId(self.kwargs["pk"])).first()
        return queryset

    def get(self, request, *args, **kwargs):
        self.data, self.statusCode = Utilities.bad_responses('not_found')

        if self.get_queryset():
            self.data, self.statusCode = Utilities.ok_response(serializer=self.list_update_serializer_class(
                self.get_queryset(), context={'request': request}).data)

        return Response(self.data, status=self.statusCode)

    def put(self, request, *args, **kwargs):
        self.data, self.statusCode = Utilities.bad_responses('not_found')

        if self.get_queryset():
            serializer = self.list_update_serializer_class(self.get_queryset(), data=request.data,
                                                           context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                self.data, self.statusCode = Utilities.ok_response('ok', serializer.data)

        return Response(self.data, self.statusCode)

    def patch(self, request, **kwargs):
        self.data, self.statusCode = Utilities.bad_responses('not_found')

        if self.get_queryset():
            serializer = self.path_serializer_class(self.get_queryset(), request.data, partial=True,
                                                    context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(status=Utilities.ok_response('patch', '')[1])

        return Response(self.data, status=self.statusCode)

    def delete(self, request, **kwargs):
        self.data, self.statusCode = Utilities.bad_responses('not_found')

        if self.get_queryset():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(self.data, status=self.statusCode)
