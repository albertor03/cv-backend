from rest_framework import serializers

from .models import JobModels


class CreateJobSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobModels
        exclude = ['created_at', 'updated_at']


class ListJobSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobModels
        fields = '__all__'
