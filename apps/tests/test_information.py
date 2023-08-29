import pytest
from bson import ObjectId
from rest_framework import status

from rest_framework.reverse import reverse
from apps.information.models import PersonalInformationModel
from apps.tests.conftest import generate_info_data


@pytest.mark.django_db
def test_01_information_str(create_information):
    info = PersonalInformationModel.objects.filter(_id=ObjectId(create_information['_id'])).first()
    assert f"{create_information['first_name']} {create_information['last_name']}" == info.__str__()


@pytest.mark.django_db
def test_02_information_no_exist(login):
    info = login.get(reverse('info'))
    assert status.HTTP_204_NO_CONTENT == info.status_code


@pytest.mark.django_db
def test_03_get_information(login, create_information):
    info = login.get(reverse('info'))
    data = info.data['data']
    error = info.data['errors']
    assert status.HTTP_200_OK == info.status_code
    assert create_information == data
    assert [] == error


@pytest.mark.django_db
def test_04_delete_information(login, create_information):
    info = login.delete(reverse('info_detail', kwargs={'pk': create_information['_id']}))
    assert status.HTTP_204_NO_CONTENT == info.status_code


@pytest.mark.django_db
def test_05_delete_an_invalid_info(login, create_information):
    info = login.delete(reverse('info_detail', kwargs={'pk': '62b5d8db1952833dd22102dd'}))
    assert status.HTTP_404_NOT_FOUND == info.status_code


@pytest.mark.django_db
def test_06_update_information(login, create_information):
    new_info = generate_info_data()
    info = login.put(reverse('info_detail', kwargs={'pk': create_information['_id']}), new_info, format='json')
    data = info.data['data']
    error = info.data['errors']
    [data.pop(x) for x in ['updated_at', 'created_at']]
    new_info['_id'] = create_information['_id']
    assert status.HTTP_200_OK == info.status_code
    assert new_info == data
    assert [] == error


@pytest.mark.django_db
def test_07_update_an_invalid_info(login, create_information):
    info = login.put(reverse('info_detail', kwargs={'pk': '62b5d8db1952833dd22102dd'}))
    assert status.HTTP_404_NOT_FOUND == info.status_code
