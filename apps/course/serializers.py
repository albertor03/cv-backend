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


# class UpdateCourseSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = CoursesModel
#         fields = '__all__'
#
#     def update(self, instance, validated_data):
#         validated_data['_id'] = ObjectId(instance.pk)
#         validated_data['updated_at'] = datetime.now()
#
#         sections = CourseSectionsModel.objects.all()
#         for section in sections:
#             course_position = 0
#             for course in section.courses:
#                 if course['_id'] == instance.pk:
#                     validated_data['created_at'] = course['created_at']
#                     if not course['certificate']:
#                         validated_data['certificate'] = ""
#
#                     section.courses[course_position] = validated_data
#                     new_courses = CourseSectionsModel.objects.filter(_id=ObjectId(section.pk)).first()
#                     new_courses.courses = section.courses
#                     new_courses.save()
#
#                 course_position += 1
#
#         CoursesModel.objects.filter(_id=ObjectId(instance.pk)).update(**validated_data)
#
#         return CoursesModel.objects.filter(_id=ObjectId(instance.pk)).first()
#
#
# class CourseSectionSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = CourseSectionsModel
#         fields = '__all__'
#
#     def create(self, validated_data):
#         new_courses = list()
#         courses = validated_data['courses']
#         for course in courses:
#             new_course = CreateCourseSerializer.Meta.model.objects.create(**course)
#             new_courses.append({'_id': new_course.pk, 'name': new_course.name, 'company': new_course.company,
#                                 'certificate': new_course.certificate, 'end_date': new_course.end_date,
#                                 'created_at': new_course.created_at, 'updated_at': new_course.updated_at,
#                                 'is_active': new_course.is_active})
#
#         if new_courses is not None:
#             validated_data['courses'] = new_courses
#
#         course_section = CourseSectionsModel.objects.create(**validated_data)
#         return course_section
#
#
class UpdateCourseSectionSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    is_active = serializers.BooleanField()

    class Meta:
        model = CourseSectionsModel
        fields = ('name', 'is_active')


# class PatchCourseSerializer(serializers.ModelSerializer):
#     course_section_id = serializers.CharField()
#     is_active = serializers.BooleanField()
#
#     class Meta:
#         model = CourseSectionsModel
#         fields = ('course_section_id', 'is_active')
#
#     def update(self, instance, validated_data):
#         sections = CourseSectionsModel.objects.all()
#         for section in sections:
#             course_position = 0
#             for course in section.courses:
#                 if course['_id'] == instance.pk:
#                     if 'course_section_id' in validated_data:
#                         course_to_change = course
#                         section.courses.pop(course_position)
#                         old_courses = CourseSectionsModel.objects.filter(_id=ObjectId(section.pk)).first()
#                         old_courses.courses = section.courses
#                         old_courses.save()
#
#                         new_courses = CourseSectionsModel.objects.filter(
#                             _id=ObjectId(validated_data['course_section_id'])).first()
#                         new_courses.courses.append(course_to_change)
#                         new_courses.save()
#                         break
#                     else:
#                         print(instance)
#                         instance.is_active = validated_data['is_active']
#                         instance.save()
#
#                         old_courses = CourseSectionsModel.objects.filter(_id=ObjectId(section.pk)).first()
#                         old_courses.courses[course_position]['is_active'] = validated_data['is_active']
#                         old_courses.save()
#                         break
#                 course_position += 1
#         return instance
