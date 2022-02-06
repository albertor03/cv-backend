from datetime import datetime

from bson import ObjectId

from .models import CourseSectionsModel, CoursesModel

from rest_framework import serializers


class ListCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoursesModel
        fields = '__all__'


class CreateCourseSerializer(serializers.ModelSerializer):
    course_section_id = serializers.CharField()

    section = str()

    class Meta:
        model = CoursesModel
        fields = '__all__'

    def validate(self, attrs):
        self.section = CourseSectionSerializer.Meta.model.objects.filter(
            _id=ObjectId(attrs['course_section_id'])).first()
        if not self.section:
            raise serializers.ValidationError({'data': {}, 'errors': ['Course Section not found.']})

        return attrs

    def create(self, validated_data):
        validated_data.pop('course_section_id')
        course = self.Meta.model.objects.create(**validated_data)
        new_course_data = {'_id': course.pk, 'name': course.name, 'company': course.company,
                           'certificate': course.certificate, 'end_date': course.end_date,
                           'created_at': course.created_at, 'updated_at': course.updated_at}
        old_course_data = self.section.courses
        if old_course_data is None:
            self.section.courses = [new_course_data]
        else:
            old_course_data.append(new_course_data)
            self.section.courses = old_course_data
        self.section.save()
        return course


class UpdateCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoursesModel
        fields = '__all__'

    def update(self, instance, validated_data):
        course_position = 0

        validated_data['_id'] = ObjectId(instance.pk)
        validated_data['updated_at'] = datetime.now()

        sections = CourseSectionsModel.objects.all()
        for section in sections:
            for course in section.courses:
                if course['_id'] == instance.pk:
                    validated_data['created_at'] = course['created_at']
                    if not course['certificate']:
                        validated_data['certificate'] = ""

                    section.courses[course_position] = validated_data
                    new_courses = CourseSectionsModel.objects.filter(_id=ObjectId(section.pk)).first()
                    new_courses.courses = section.courses
                    new_courses.save()

                course_position += 1

        CoursesModel.objects.filter(_id=ObjectId(instance.pk)).update(**validated_data)

        return instance


class CourseSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseSectionsModel
        fields = '__all__'

    def create(self, validated_data):
        new_courses = list()
        courses = validated_data['courses']
        for course in courses:
            new_course = CreateCourseSerializer.Meta.model.objects.create(**course)
            new_courses.append({'_id': new_course.pk, 'name': new_course.name, 'company': new_course.company,
                                'certificate': new_course.certificate, 'end_date': new_course.end_date,
                                'created_at': new_course.created_at, 'updated_at': new_course.updated_at})

        if new_courses is not None:
            validated_data['courses'] = new_courses

        course_section = CourseSectionsModel.objects.create(**validated_data)
        return course_section


class UpdateCourseSectionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)

    class Meta:
        model = CourseSectionsModel
        fields = ('name', )


class PatchCourseSerializer(serializers.ModelSerializer):
    course_section_id = serializers.CharField(required=True)

    class Meta:
        model = CourseSectionsModel
        fields = ('course_section_id',)

    def update(self, instance, validated_data):
        print(instance.pk, validated_data)

        return instance
