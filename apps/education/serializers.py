from .models import EducationModels

from rest_framework import serializers


class EducationSerializer(serializers.ModelSerializer):

    class Meta:
        model = EducationModels
        fields = '__all__'


class CreateEducationSerializer(serializers.ModelSerializer):

    class Meta:
        model = EducationModels
        exclude = ['created_at', 'updated_at']
