from bson import ObjectId

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response

from .serializers import (
    ListSkillSerializer,
    CreateSkillSerializer
)
from ..Utilities.utilities import Utilities


class ListCreateSkillAPIView(generics.ListCreateAPIView):
    serializer_class = ListSkillSerializer
    list_serializer_class = CreateSkillSerializer
    data, statusCode = Utilities.bad_responses('bad_request')

    def get(self, request, **kwargs):
        serializer = self.serializer_class(self.get_serializer().Meta.model.objects.all(),
                                           many=True, context={'request': request})

        self.data, self.statusCode = Utilities.ok_response('ok', serializer.data)
        self.data['total_skills'] = len(serializer.data)

        return Response(self.data, status=self.statusCode)

    def post(self, request, *args, **kwargs):
        self.data.clear()
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            self.data, self.statusCode = Utilities.ok_response(
                'post', self.list_serializer_class(serializer.save(), context={'request': request}).data)

        return Response(self.data, self.statusCode)


class RetrieveUpdateDestroySkillAPIView(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        queryset = self.serializer_class().Meta.model.objects.filter(_id=ObjectId(self.kwargs["pk"])).first()
        return queryset

    serializer_class = ListSkillSerializer
    data, statusCode = Utilities.bad_responses('bad_request')

    def get(self, request, **kwargs):
        skill = self.get_queryset()
        self.data, self.statusCode = Utilities.bad_responses('not_found')

        if skill:
            self.data, self.statusCode = Utilities.ok_response(
                'ok', self.serializer_class(skill, context={'request': request}).data)

        return Response(self.data, status=self.statusCode)

    def put(self, request, **kwargs):
        skill = self.get_queryset()
        self.data, self.statusCode = Utilities.bad_responses('not_found')

        if skill:
            serializer = self.serializer_class(skill, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                self.data, self.statusCode = Utilities.ok_response('ok', serializer.data)

        return Response(self.data, status=self.statusCode)

    def patch(self, request, **kwargs):
        skill = self.get_queryset()
        self.data, self.statusCode = Utilities.bad_responses('not_found')
        if skill:
            serializer = self.serializer_class(skill, request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                self.data, self.statusCode = Utilities.ok_response('ok', serializer.data)

        return Response(self.data, status=self.statusCode)

    def delete(self, request, **kwargs):
        skill = self.get_queryset()
        self.data, self.statusCode = Utilities.bad_responses('not_found')
        if skill:
            skill.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(self.data, status=self.statusCode)
