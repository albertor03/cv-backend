from bson import ObjectId
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response

from .serializers import PersonalInformationSerializer, PersonalInformationModel
from ..Utilities.utilities import Utilities


class PersonalInformationAPIView(generics.CreateAPIView):
    queryset = PersonalInformationModel.objects.all()
    serializer_class = PersonalInformationSerializer
    data, statusCode = Utilities.bad_responses('bad_request')

    def get(self, request, **kwargs):
        info = self.get_queryset().first()
        self.data, self.statusCode = Utilities.bad_responses('not_found')

        if info:
            self.data, self.statusCode = Utilities.ok_response('ok', self.serializer_class(info).data)

        return Response(self.data, status=self.statusCode)

    def post(self, request, **kwargs):
        info = self.get_queryset()
        self.data, self.statusCode = Utilities.bad_responses('information_recorded')

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if not info:
                serializer.save()
                self.data, self.statusCode = Utilities.ok_response('post', serializer.data)

        return Response(self.data, status=self.statusCode)


class PersonalInformationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        queryset = PersonalInformationModel.objects.filter(_id=ObjectId(self.kwargs['pk'])).first()
        return queryset

    serializer_class = PersonalInformationSerializer
    data, statusCode = Utilities.bad_responses('bad_request')
    http_method_names = ['put', 'delete']

    def put(self, request, **kwargs):
        info = self.get_queryset()
        self.data, self.statusCode = Utilities.bad_responses('not_found')

        if info:
            serializer = self.serializer_class(info, data=request.data)
            if serializer.is_valid():
                serializer.save()
                self.data, self.statusCode = Utilities.ok_response('ok', serializer.data)

        return Response(self.data, status=self.statusCode)

    def delete(self, request, **kwargs):
        user = self.get_queryset()
        self.data, self.statusCode = Utilities.bad_responses('not_found')
        if user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(self.data, status=self.statusCode)
