from bson import ObjectId

from .models import CourseSectionsModel, CoursesModel

from rest_framework import serializers


class ListUpdateCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoursesModel
        fields = '__all__'

    def update(self, instance, validated_data):
        data = self.Meta.model.objects.filter(_id=ObjectId(instance.pk)).first()
        if data.certificate.name:
            data.certificate.delete(data.certificate.name)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance


class CreateCourseSectionSerializer(serializers.ModelSerializer):
    courses = ListUpdateCourseSerializer(many=True, read_only=True)

    class Meta:
        model = CourseSectionsModel
        fields = '__all__'

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
        fields = '__all__'

    def validate(self, attrs):
        self.section = self.Meta.model.objects.filter(_id=ObjectId(attrs['course_section_id'])).first()
        if not self.section:
            raise serializers.ValidationError({'data': {}, 'errors': ['Course Section not found.']})

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


class PatchCourseSerializer(serializers.ModelSerializer):
    course_section_id = serializers.CharField()
    is_active = serializers.BooleanField()

    class Meta:
        model = CourseSectionsModel
        fields = ('course_section_id', 'is_active')

    def update(self, instance, validated_data):
        if validated_data.get('course_section_id', ''):
            sections = self.Meta.model.objects.all()

            course_section_position = 0
            for section in sections:
                if instance.pk in section.courses_id:
                    section.courses_id.remove(instance.pk)

                if ObjectId(validated_data['course_section_id']) == section.pk:
                    section.courses_id.add(instance.pk)

                course_section_position += 1
                section.save()
        else:
            instance.is_active = validated_data['is_active']
            instance.save()

        return instance
