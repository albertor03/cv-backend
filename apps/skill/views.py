from bson import ObjectId

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response

from .serializers import (
    ListSkillSerializer,
    CreateSkillSerializer
)


class ListCreateSkillAPIView(generics.ListCreateAPIView):
    serializer_class = ListSkillSerializer
    list_serializer_class = CreateSkillSerializer
    statusCode = status.HTTP_400_BAD_REQUEST
    data = {'data': {}, 'errors': ['Information not found.']}

    def get(self, request, **kwargs):
        skill = self.get_serializer().Meta.model.objects.all()
        skill_serializer = self.serializer_class(skill, many=True, context={'request': request})

        self.data['data'] = skill_serializer.data
        self.data['errors'].clear()
        self.statusCode = status.HTTP_200_OK
        return Response(self.data, status=self.statusCode)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            skill = serializer.save()
            self.data['data'] = self.list_serializer_class(skill, context={'request': request}).data
            self.data['errors'].clear()
            self.statusCode = status.HTTP_201_CREATED

        return Response(self.data, self.statusCode)


class RetrieveUpdateDestroySkillAPIView(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        queryset = self.serializer_class().Meta.model.objects.filter(_id=ObjectId(self.kwargs["pk"])).first()
        return queryset

    serializer_class = ListSkillSerializer
    data = {'data': {}, 'errors': ['Information not found.']}
    statusCode = status.HTTP_400_BAD_REQUEST
    http_method_names = ['get', 'put', 'delete']

    def get(self, request, **kwargs):
        skill = self.get_queryset()
        self.statusCode = status.HTTP_404_NOT_FOUND

        if skill:
            skill_serializer = self.serializer_class(skill, context={'request': request})
            self.data["data"] = skill_serializer.data
            self.data["errors"].clear()
            self.statusCode = status.HTTP_200_OK

        return Response(self.data, status=self.statusCode)

    def put(self, request, **kwargs):
        skill = self.get_queryset()
        self.statusCode = status.HTTP_404_NOT_FOUND

        if skill:
            serializer = self.serializer_class(skill, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                self.data["data"] = serializer.data
                self.data["errors"].clear()
                self.statusCode = status.HTTP_200_OK

        return Response(self.data, status=self.statusCode)

    def patch(self, request, **kwargs):
        skill = self.get_queryset()
        if skill:
            serializer = self.serializer_class(skill, request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                self.data["data"] = serializer.data
                self.data["errors"].clear()
                self.statusCode = status.HTTP_200_OK

        return Response(self.data, status=self.statusCode)

    def delete(self, request, **kwargs):
        skill = self.get_queryset()
        self.statusCode = status.HTTP_404_NOT_FOUND
        if skill:
            skill.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(self.data, status=self.statusCode)
