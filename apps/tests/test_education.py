import pytest
from bson import ObjectId
from rest_framework import status

from rest_framework.reverse import reverse

from apps.education.models import EducationModels
from apps.tests.conftest import generate_education_data


@pytest.mark.django_db
def test_01_education_str(create_education):
    education_data = EducationModels.objects.filter(_id=ObjectId(create_education['_id'])).first()
    assert f"{create_education['degree']} in {create_education['collage']}" == education_data.__str__()


@pytest.mark.django_db
def test_02_end_date_less_than_start_date(login):
    new_education = generate_education_data("less")
    response_data = login.post(reverse('list_create_education'), new_education)
    data = response_data.data['data']
    errors = response_data.data['errors']
    assert status.HTTP_400_BAD_REQUEST == response_data.status_code
    assert {} == data
    assert ['The end date field must not be less than the start date field.'] == errors


@pytest.mark.django_db
def test_03_get_education_data(login, create_education):
    response_data = login.get(reverse('retrieve_update_destroy_education', kwargs={'pk': create_education['_id']}))
    data = response_data.data['data']
    errors = response_data.data['errors']
    assert status.HTTP_200_OK == response_data.status_code
    assert create_education == data
    assert [] == errors


@pytest.mark.django_db
def test_04_update_education_data(login, create_education):
    new_education = generate_education_data()
    response_data = login.put(reverse('retrieve_update_destroy_education', kwargs={'pk': create_education['_id']}), new_education)
    [response_data.data['data'].pop(x) for x in ['created_at', 'updated_at']]
    data = response_data.data['data']
    errors = response_data.data['errors']
    new_education['_id'] = create_education['_id']
    assert status.HTTP_200_OK == response_data.status_code
    assert new_education == data
    assert [] == errors


@pytest.mark.django_db
def test_05_patch_education_data(login, create_education):
    response_data = login.patch(reverse('retrieve_update_destroy_education', kwargs={'pk': create_education['_id']}), dict(is_active=True))
    data = response_data.data['data']
    errors = response_data.data['errors']
    create_education['is_active'] = True
    assert status.HTTP_200_OK == response_data.status_code
    assert create_education == data
    assert [] == errors


@pytest.mark.django_db
def test_06_delete_education_data(login, create_education):
    response_data = login.delete(reverse('retrieve_update_destroy_education', kwargs={'pk': create_education['_id']}))
    assert status.HTTP_204_NO_CONTENT == response_data.status_code


@pytest.mark.django_db
def test_07_get_all_education_data(login, create_education):
    response_data = login.get(reverse('list_create_education'))
    data = response_data.data['data'][0]
    errors = response_data.data['errors']
    total = response_data.data['total_educations']
    assert status.HTTP_200_OK == response_data.status_code
    assert create_education == data
    assert [] == errors
    assert total >= 1


@pytest.mark.django_db
def test_08_attempt_get_education_data(login):
    response_data = login.get(reverse('retrieve_update_destroy_education', kwargs={'pk': '62b5d8db1952833dd22102dd'}))
    data = response_data.data['data']
    errors = response_data.data['errors']
    assert status.HTTP_404_NOT_FOUND == response_data.status_code
    assert {} == data
    assert ["Information not found."] == errors


@pytest.mark.django_db
def test_09_attempt_register_education_data_with_an_invalid_certificate_value(login):
    new_data = generate_education_data('base64')
    response_data = login.post(reverse('list_create_education'), new_data)
    data = response_data.data['data']
    errors = response_data.data['errors']
    assert status.HTTP_400_BAD_REQUEST == response_data.status_code
    assert {} == data
    assert ["The certificate field must be base64."] == errors
