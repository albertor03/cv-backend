from rest_framework import serializers

from .models import PersonalInformationModel


class PersonalInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonalInformationModel
        fields = [
            '_id', 'first_name', 'last_name', 'email', 'profession', 'phone', 'address', 'created_at', 'updated_at'
        ]
