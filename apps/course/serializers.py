from .models import CourseSectionsModel, CoursesModel

from rest_framework import serializers


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoursesModel
        fields = '__all__'


class CourseSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseSectionsModel
        fields = '__all__'
