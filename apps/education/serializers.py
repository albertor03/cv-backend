from bson import ObjectId

from .models import EducationModels

from rest_framework import serializers


class EducationSerializer(serializers.ModelSerializer):

    class Meta:
        model = EducationModels
        fields = '__all__'


class UpdateEducationSerializer(serializers.ModelSerializer):

    class Meta:
        model = EducationModels
        fields = '__all__'

    def update(self, instance, validated_data):
        education = EducationModels.objects.filter(_id=ObjectId(instance.pk)).first()
        if education.certificate.name:
            education.certificate.delete(education.certificate.name)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance


class CreateEducationSerializer(serializers.ModelSerializer):

    class Meta:
        model = EducationModels
        exclude = ['created_at', 'updated_at']
