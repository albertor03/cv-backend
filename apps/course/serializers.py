import base64

from bson import ObjectId
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from .models import CourseSectionsModel, CoursesModel


class ListUpdateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursesModel
        exclude = ['created_at', 'updated_at']


class CreateCourseSectionSerializer(serializers.ModelSerializer):
    courses = ListUpdateCourseSerializer(many=True, read_only=True)

    def get_query(self, pk):
        try:
            pk = ObjectId(pk)
        except:
            raise serializers.ValidationError(dict(data={}, errors=['The id received has an invalid format.']))

        data = CourseSectionsModel.objects.all().filter(_id=pk).first()
        if not data:
            raise NotFound({'data': {}, 'errors': ['Course Section not found.']})
        return data

    class Meta:
        model = CourseSectionsModel
        exclude = ['created_at', 'updated_at']

    def create(self, validated_data):
        courses_list = self.initial_data.pop('courses', [])
        course_instance = self.Meta.model.objects.create(**validated_data)

        for course in courses_list:
            course_saved = CoursesModel.objects.create(**course)
            course_instance.courses.add(CoursesModel.objects.filter(_id=course_saved._id).first())

        course_instance.save()
        return course_instance


class CreateCourseSerializer(serializers.ModelSerializer):
    course_section_id = serializers.CharField()

    section = str()

    class Meta:
        model = CoursesModel
        exclude = ['created_at', 'updated_at']

    def get_query(self, pk):
        try:
            pk = ObjectId(pk)
        except:
            raise serializers.ValidationError(dict(data={}, errors=['The id received has an invalid format.']))

        data = CoursesModel.objects.filter(_id=pk).first()
        if not data:
            raise NotFound(detail=dict(data={}, errors=['Course not found.']))

        return data

    def validate(self, attrs):
        try:
            pk = ObjectId(attrs['course_section_id'])
        except:
            raise serializers.ValidationError(dict(data={}, errors=['The id received has an invalid format.']))

        self.section = CourseSectionsModel.objects.filter(_id=pk).first()
        if not self.section:
            raise NotFound({'data': {}, 'errors': ['Course Section not found.']})

        if 'certificate' in attrs and self.context['request'].method != 'PATCH':
            try:
                base64.b64decode(attrs['certificate'], validate=True)
            except:
                raise serializers.ValidationError(
                    detail={'data': {}, 'errors': ['The certificate field must be base64.']})

        return attrs

    def create(self, validated_data):
        validated_data.pop('course_section_id')
        course = self.Meta.model.objects.create(**validated_data)
        self.section.courses.add(course)
        self.section.save()
        return course


class UpdateCourseSectionSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    is_active = serializers.BooleanField()

    class Meta:
        model = CourseSectionsModel
        fields = ('name', 'is_active')

    def validate(self, attrs):
        if len(attrs) == 0:
            raise serializers.ValidationError(
                detail=dict(data={}, errors=[f"The {self.Meta.fields} fields are required."]))
        return attrs


class PatchCourseSerializer(serializers.ModelSerializer):
    course_section_id = serializers.CharField()
    is_active = serializers.BooleanField()

    class Meta:
        model = CourseSectionsModel
        fields = ('course_section_id', 'is_active')

    def validate(self, attrs):
        if len(attrs.keys()) == 0:
            raise serializers.ValidationError(
                detail=dict(data={}, errors=[f"The {self.Meta.fields} fields are required."]))
        elif len(attrs.keys()) > 1:
            raise serializers.ValidationError(
                detail=dict(data={}, errors=[f"Only one of the fields can be sent at a time. Accepted fields:"
                                             f" {self.Meta.fields}"]))

        return attrs

    def update(self, instance, validated_data):
        if 'course_section_id' in validated_data:
            sections = self.Meta.model.objects.all()
            for section in sections:
                if instance.pk in section.courses_id:
                    section.courses_id.remove(instance.pk)

                if ObjectId(validated_data['course_section_id']) == section.pk:
                    section.courses_id.add(instance.pk)

                section.save()
        else:
            instance.is_active = validated_data['is_active']
            instance.save()

        return instance
