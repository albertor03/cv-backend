from bson import ObjectId
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response

from .serializers import PersonalInformationSerializer, PersonalInformationModel


class PersonalInformationAPIView(generics.ListCreateAPIView):
    serializer_class = PersonalInformationSerializer
    data = {'data': {}, 'errors': []}
    statusCode = status.HTTP_400_BAD_REQUEST

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.all()

    def post(self, request, **kwargs):
        info = self.get_queryset()
        self.data = {'data': {}, 'errors': ['There is information recorded.']}
        self.statusCode = status.HTTP_406_NOT_ACCEPTABLE
        serializer = PersonalInformationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if not info:
                serializer.save()
                self.data['data'] = serializer.data
                self.data['errors'] = []
                self.statusCode = status.HTTP_201_CREATED

        return Response(self.data, status=self.statusCode)


class PersonalInformationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PersonalInformationSerializer
    data = {'data': {}, 'errors': []}
    statusCode = status.HTTP_400_BAD_REQUEST

    @staticmethod
    def get_object(pk=None):
        return PersonalInformationModel.objects.filter(_id=ObjectId(pk)).first()

    def get(self, request, pk=None, **kwargs):
        info = self.get_object(pk)
        self.data = {'data': {}, 'errors': ['Information not found.']}
        self.statusCode = status.HTTP_404_NOT_FOUND

        if info:
            info_serializer = PersonalInformationSerializer(info)
            self.data["data"] = info_serializer.data
            self.data["errors"] = []
            self.statusCode = status.HTTP_200_OK

        return Response(self.data, status=self.statusCode)

    def put(self, request, pk=None, **kwargs):
        info = self.get_object(pk)
        self.data = {'data': {}, 'errors': ['Information not found.']}
        self.statusCode = status.HTTP_404_NOT_FOUND

        if info:
            serializer = PersonalInformationSerializer(info, data=request.data)
            if serializer.is_valid():
                serializer.save()
                self.data["data"] = serializer.data
                self.data["errors"] = []
                self.statusCode = status.HTTP_200_OK

        return Response(self.data, status=self.statusCode)

    def delete(self, request, pk=None, **kwargs):
        user = self.get_object(pk)
        self.data = {'data': {}, 'errors': ['Information not found.']}
        self.statusCode = status.HTTP_404_NOT_FOUND
        if user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(self.data, status=self.statusCode)
