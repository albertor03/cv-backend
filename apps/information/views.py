from bson import ObjectId
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response

from .serializers import PersonalInformationSerializer, PersonalInformationModel


class PersonalInformationAPIView(generics.CreateAPIView):
    queryset = PersonalInformationModel.objects.all()
    serializer_class = PersonalInformationSerializer
    statusCode = status.HTTP_400_BAD_REQUEST

    def get(self, request, **kwargs):
        info = self.get_queryset().first()
        data = {'data': {}, 'errors': ['Information not found.']}
        self.statusCode = status.HTTP_404_NOT_FOUND

        if info:
            info_serializer = self.serializer_class(info)
            data["data"] = info_serializer.data
            data["errors"].clear()
            self.statusCode = status.HTTP_200_OK

        return Response(data, status=self.statusCode)

    def post(self, request, **kwargs):
        info = self.get_queryset()
        data = {'data': {}, 'errors': ['There is information recorded.']}
        self.statusCode = status.HTTP_406_NOT_ACCEPTABLE
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if not info:
                serializer.save()
                data['data'] = serializer.data
                data['errors'] = []
                self.statusCode = status.HTTP_201_CREATED

        return Response(data, status=self.statusCode)


class PersonalInformationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        queryset = PersonalInformationModel.objects.filter(_id=ObjectId(self.kwargs['pk'])).first()
        return queryset

    serializer_class = PersonalInformationSerializer
    data = {'data': {}, 'errors': []}
    statusCode = status.HTTP_400_BAD_REQUEST
    http_method_names = ['put', 'delete']

    def put(self, request, **kwargs):
        info = self.get_queryset()
        data = {'data': {}, 'errors': ['Information not found.']}
        self.statusCode = status.HTTP_404_NOT_FOUND

        if info:
            serializer = self.serializer_class(info, data=request.data)
            if serializer.is_valid():
                serializer.save()
                data["data"] = serializer.data
                data["errors"].clear()
                self.statusCode = status.HTTP_200_OK

        return Response(data, status=self.statusCode)

    def delete(self, request, **kwargs):
        user = self.get_queryset()
        data = {'data': {}, 'errors': ['Information not found.']}
        self.statusCode = status.HTTP_404_NOT_FOUND
        if user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(data, status=self.statusCode)
