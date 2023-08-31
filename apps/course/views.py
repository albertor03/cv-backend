from rest_framework import generics
from rest_framework import status
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

    def patch(self, request, *args, **kwargs):
        data = self.serializer_class().get_query(self.kwargs["pk"])
        serializer = self.update_serializer_class(data, request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            section = serializer.save()
            self.data, self.statusCode = Utilities.ok_response(serializer=self.serializer_class(section).data)

        return Response(self.data, status=self.statusCode)

    def delete(self, request, **kwargs):
        self.serializer_class().get_query(self.kwargs["pk"]).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        self.data.clear()
        serializer = self.serializer_class(data=request.data, context={'request': request})
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

    def get(self, request, *args, **kwargs):
        data = self.serializer_class().get_query(self.kwargs['pk'])
        self.data, self.statusCode = Utilities.ok_response(serializer=self.list_update_serializer_class(
            data, context={'request': request}).data)

        return Response(self.data, status=self.statusCode)

    def put(self, request, *args, **kwargs):
        serializer = self.list_update_serializer_class(self.serializer_class().get_query(self.kwargs['pk']),
                                                       data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            self.data, self.statusCode = Utilities.ok_response('ok', serializer.data)

        return Response(self.data, self.statusCode)

    def patch(self, request, **kwargs):
        serializer = self.path_serializer_class(self.serializer_class().get_query(self.kwargs['pk']), request.data,
                                                partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, **kwargs):
        self.serializer_class().get_query(self.kwargs['pk']).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
