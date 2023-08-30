import base64

from bson import ObjectId
from rest_framework.exceptions import NotFound

from .models import EducationModels

from rest_framework import serializers


class EducationSerializer(serializers.ModelSerializer):

    def get_query(self, pk):
        data = EducationModels.objects.filter(_id=ObjectId(pk)).first()
        if not data:
            raise NotFound({'data': {}, 'errors': ['Information not found.']})
        return data

    class Meta:
        model = EducationModels
        fields = '__all__'

    def validate(self, attrs):
        if 'end_date' in attrs and attrs['end_date'] is not None:
            if attrs['end_date'] < attrs['start_date']:
                raise serializers.ValidationError(detail={'data': {}, 'errors': ['The end date field must not be less than the start date field.']})

        if 'certificate' in attrs and self.context['request'].method != 'PATCH':
            try:
                base64.b64decode(attrs['certificate'], validate=True)
            except:
                raise serializers.ValidationError(detail={'data': {}, 'errors': ['The certificate field must be base64.']})

        return attrs
