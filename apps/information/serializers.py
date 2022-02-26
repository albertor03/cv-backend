from rest_framework import serializers

from .models import PersonalInformationModel


class PersonalInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonalInformationModel
        fields = '__all__'
