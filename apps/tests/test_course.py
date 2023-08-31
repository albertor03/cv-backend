import pytest
from bson import ObjectId
from rest_framework import status
from rest_framework.reverse import reverse

from apps.course.models import CourseSectionsModel, CoursesModel
from apps.course.serializers import UpdateCourseSectionSerializer, PatchCourseSerializer
from apps.tests.conftest import generate_course_section_data, generate_course_data


@pytest.mark.django_db
def test_01_course_section_str(create_course_section):
    course_section_data = CourseSectionsModel.objects.filter(_id=ObjectId(create_course_section['_id'])).first()
    assert f"{create_course_section['name']}" == course_section_data.__str__()


@pytest.mark.django_db
def test_02_get_all_course_section(login, create_course_section):
    response_data = login.get(reverse('list_create_course_section'))
    data = response_data.data['data'][0]
    errors = response_data.data['errors']
    total_sections = response_data.data['total_course_sections']
    assert status.HTTP_200_OK == response_data.status_code
    assert create_course_section == data
    assert [] == errors
    assert total_sections >= 1


@pytest.mark.django_db
def test_03_change_course_section_name(login, create_course_section):
    name = generate_course_section_data()['name']
    response_data = login.patch(reverse('detail_course_section', kwargs={'pk': create_course_section['_id']}),
                                dict(name=name))
    data = response_data.data['data']
    errors = response_data.data['errors']
    create_course_section['name'] = name
    assert status.HTTP_200_OK == response_data.status_code
    assert create_course_section == data
    assert [] == errors


@pytest.mark.django_db
def test_04_active_a_course_section(login, create_course_section):
    is_active = True
    response_data = login.patch(reverse('detail_course_section', kwargs={'pk': create_course_section['_id']}),
                                dict(is_active=is_active))
    data = response_data.data['data']
    errors = response_data.data['errors']
    create_course_section['is_active'] = is_active
    assert status.HTTP_200_OK == response_data.status_code
    assert create_course_section == data
    assert [] == errors


@pytest.mark.django_db
def test_05_delete_a_course_section(login, create_course_section):
    response_data = login.delete(reverse('detail_course_section', kwargs={'pk': create_course_section['_id']}))
    assert status.HTTP_204_NO_CONTENT == response_data.status_code


@pytest.mark.django_db
def test_06_patch_an_invalid_course_section(login, create_course_section):
    response_data = login.patch(reverse('detail_course_section', kwargs={'pk': '62b5d8db1952833dd22102dd'}))
    data = response_data.data['data']
    errors = response_data.data['errors']
    assert status.HTTP_404_NOT_FOUND == response_data.status_code
    assert {} == data
    assert ['Course Section not found.'] == errors


@pytest.mark.django_db
def test_07_create_a_course_section_with_courses(login):
    new_course_section = generate_course_section_data('with')
    response_data = login.post(reverse('list_create_course_section'), new_course_section, format='json')
    course_data = dict(response_data.data['data'].pop('courses')[0])
    [course_data.pop(x) for x in ['_id']]
    errors = response_data.data['errors']
    assert status.HTTP_201_CREATED == response_data.status_code
    assert new_course_section['courses'][0] == course_data
    assert [] == errors


@pytest.mark.django_db
def test_08_create_a_course(create_course):
    assert create_course['_id']


@pytest.mark.django_db
def test_09_create_a_course_with_an_invalid_course_section(login):
    course_data = generate_course_data()
    course_data['course_section_id'] = str(ObjectId())
    response_data = login.post(reverse('list_create_course'), course_data, format='json')
    data = response_data.data['data']
    errors = response_data.data['errors']
    assert status.HTTP_404_NOT_FOUND == response_data.status_code
    assert {} == data
    assert ['Course Section not found.'] == errors


@pytest.mark.django_db
def test_10_create_a_course_with_an_invalid_value_in_certificate_field(login, create_course_section):
    course_data = generate_course_data("invalid")
    course_data['course_section_id'] = create_course_section['_id']
    response_data = login.post(reverse('list_create_course'), course_data, format='json')
    data = response_data.data['data']
    errors = response_data.data['errors']
    assert status.HTTP_400_BAD_REQUEST == response_data.status_code
    assert {} == data
    assert ['The certificate field must be base64.'] == errors


@pytest.mark.django_db
def test_11_update_course_section_without_required_fields(login, create_course_section):
    response_data = login.patch(reverse('detail_course_section', kwargs={'pk': create_course_section['_id']}),
                                {}, format='json')
    data = response_data.data['data']
    errors = response_data.data['errors']
    assert status.HTTP_400_BAD_REQUEST == response_data.status_code
    assert {} == data
    assert [f"The {UpdateCourseSectionSerializer.Meta.fields} fields are required."] == errors


@pytest.mark.django_db
def test_12_update_course_without_required_fields(login, create_course):
    response_data = login.patch(reverse('detail_course', kwargs={'pk': create_course['_id']}),
                                {}, format='json')
    data = response_data.data['data']
    errors = response_data.data['errors']
    assert status.HTTP_400_BAD_REQUEST == response_data.status_code
    assert {} == data
    assert [f"The {PatchCourseSerializer.Meta.fields} fields are required."] == errors


@pytest.mark.django_db
def test_13_update_course_with_more_of_one_required_fields(login, create_course):
    response_data = login.patch(reverse('detail_course', kwargs={'pk': create_course['_id']}),
                                dict(course_section_id=str(ObjectId), is_active=True), format='json')
    data = response_data.data['data']
    errors = response_data.data['errors']
    assert status.HTTP_400_BAD_REQUEST == response_data.status_code
    assert {} == data
    assert [f"Only one of the fields can be sent at a time. Accepted fields:"
            f" {PatchCourseSerializer.Meta.fields}"] == errors


@pytest.mark.django_db
def test_14_update_course_with_required_fields(login, create_course):
    response_data = login.patch(reverse('detail_course', kwargs={'pk': create_course['_id']}),
                                dict(is_active=True), format='json')
    assert status.HTTP_204_NO_CONTENT == response_data.status_code


@pytest.mark.django_db
def test_15_attempt_update_a_invalid_course(login):
    response_data = login.patch(reverse('detail_course', kwargs={'pk': str(ObjectId())}),
                                dict(is_active=True), format='json')
    assert status.HTTP_404_NOT_FOUND == response_data.status_code
    assert {} == response_data.data['data']
    assert ["Course not found."] == response_data.data['errors']


@pytest.mark.django_db
def test_16_update_course_section_of_course(login, create_course, create_course_section):
    response_data = login.patch(reverse('detail_course', kwargs={'pk': create_course['_id']}),
                                dict(course_section_id=create_course_section['_id']), format='json')
    assert status.HTTP_204_NO_CONTENT == response_data.status_code


@pytest.mark.django_db
def test_17_attempt_update_invalid_course_section(login):
    response_data = login.patch(reverse('detail_course_section', kwargs={'pk': str(ObjectId())}),
                                dict(is_active=True), format='json')
    assert status.HTTP_404_NOT_FOUND == response_data.status_code
    assert {} == response_data.data['data']
    assert ["Course Section not found."] == response_data.data['errors']


@pytest.mark.django_db
def test_18_attempt_update_invalid_course_section_id(login):
    response_data = login.patch(reverse('detail_course_section', kwargs={'pk': "test"}),
                                dict(is_active=True), format='json')
    assert status.HTTP_400_BAD_REQUEST == response_data.status_code
    assert {} == response_data.data['data']
    assert ["The id received has an invalid format."] == response_data.data['errors']


@pytest.mark.django_db
def test_19_create_a_course_with_an_invalid_course_section(login):
    course_data = generate_course_data()
    course_data['course_section_id'] = "test"
    response_data = login.post(reverse('list_create_course'), course_data, format='json')
    data = response_data.data['data']
    errors = response_data.data['errors']
    assert status.HTTP_400_BAD_REQUEST == response_data.status_code
    assert {} == data
    assert ["The id received has an invalid format."] == errors


@pytest.mark.django_db
def test_20_get_a_course_with_an_invalid_course_section(login):
    response_data = login.get(reverse('detail_course', kwargs={'pk': 'test'}))
    data = response_data.data['data']
    errors = response_data.data['errors']
    assert status.HTTP_400_BAD_REQUEST == response_data.status_code
    assert {} == data
    assert ["The id received has an invalid format."] == errors


@pytest.mark.django_db
def test_21_get_all_courses(login, create_course):
    response_data = login.get(reverse('list_create_course'))
    data = response_data.data['data'][0]
    errors = response_data.data['errors']
    total = response_data.data['total_courses']
    assert status.HTTP_200_OK == response_data.status_code
    assert create_course == data
    assert [] == errors
    assert total >= 1


@pytest.mark.django_db
def test_22_get_one_courses(login, create_course):
    response_data = login.get(reverse('detail_course', kwargs={'pk': create_course['_id']}))
    data = response_data.data['data']
    errors = response_data.data['errors']
    assert status.HTTP_200_OK == response_data.status_code
    assert create_course == data
    assert [] == errors


@pytest.mark.django_db
def test_23_update_one_courses(login, create_course):
    new_course = generate_course_data()
    response_data = login.put(reverse('detail_course', kwargs={'pk': create_course['_id']}), new_course)
    data = response_data.data['data']
    errors = response_data.data['errors']
    new_course['_id'] = create_course['_id']
    assert status.HTTP_200_OK == response_data.status_code
    assert new_course == data
    assert [] == errors


@pytest.mark.django_db
def test_24_delete_one_courses(login, create_course):
    response_data = login.delete(reverse('detail_course', kwargs={'pk': create_course['_id']}))
    assert status.HTTP_204_NO_CONTENT == response_data.status_code


@pytest.mark.django_db
def test_25_course_str(create_course):
    create_course_data = CoursesModel.objects.filter(_id=ObjectId(create_course['_id'])).first()
    assert f"{create_course['name']} in {create_course['company']}" == create_course_data.__str__()


@pytest.mark.django_db
def test_26_delete_a_course_section_with_course(login, create_course_section):
    course = generate_course_data()
    course['course_section_id'] = create_course_section['_id']
    login.post(reverse('list_create_course'), course, format='json').data['data']
    response_data = login.delete(reverse('detail_course_section', kwargs={'pk': create_course_section['_id']}))
    assert status.HTTP_204_NO_CONTENT == response_data.status_code
