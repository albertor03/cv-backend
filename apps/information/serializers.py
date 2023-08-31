from rest_framework import serializers

from .models import PersonalInformationModel


class PersonalInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonalInformationModel
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['contact_info'] = instance.contact_info
        representation['contact_social'] = instance.contact_social
        return representation
