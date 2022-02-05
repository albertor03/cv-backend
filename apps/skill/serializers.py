from rest_framework import serializers

from .models import SkillModel


class ListSkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = SkillModel
        fields = '__all__'


class CreateSkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = SkillModel
        exclude = ['created_at', 'updated_at']
