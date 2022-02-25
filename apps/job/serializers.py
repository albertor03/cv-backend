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


class ActiveJobSerializer(serializers.ModelSerializer):

    is_active = serializers.BooleanField()

    class Meta:
        model = JobModels
        fields = '__all__'

    def validate(self, attrs):
        if 'is_active' not in attrs:
            raise serializers.ValidationError({'data': {}, 'errors': ['The is active field must match.']})

        return attrs
