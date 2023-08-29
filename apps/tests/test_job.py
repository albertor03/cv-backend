from datetime import datetime

import pytest
from rest_framework import status

from rest_framework.reverse import reverse
from apps.job.models import JobModels
from apps.tests.conftest import generate_job_data


@pytest.mark.django_db
def test_01_job_str(create_job):
    job_name = JobModels.objects.filter(position=create_job['position']).first()
    assert f"{create_job['position']} {create_job['company_name']}" == job_name.__str__()


@pytest.mark.django_db
def test_02_create_a_new_job_default(login):
    new_job = generate_job_data("default")
    response = login.post(reverse('list_create_job'), new_job)
    response_data = response.data['data']
    errors = response.data['errors']
    [response_data.pop(x) for x in ['_id', 'is_active']]
    for item in ['start_date', 'end_date']:
        response_data[item] = datetime.fromtimestamp(int(response_data[item])).strftime('%Y-%m-%d')
        new_job[item] = new_job[item].strftime('%Y-%m-%d')

    assert status.HTTP_201_CREATED == response.status_code
    assert new_job == response_data
    assert [] == errors


@pytest.mark.django_db
def test_03_create_a_new_job_inactive_and_without_end_date(login):
    new_job = generate_job_data("without")
    response = login.post(reverse('list_create_job'), new_job)
    response_data = response.data['data']
    errors = response.data['errors']
    [response_data.pop(x) for x in ['_id', 'is_active']]
    response_data['start_date'] = datetime.fromtimestamp(int(response_data['start_date'])).strftime('%Y-%m-%d')
    new_job['start_date'] = new_job['start_date'].strftime('%Y-%m-%d')
    new_job['end_date'] = None
    new_job['currently'] = False
    assert status.HTTP_201_CREATED == response.status_code
    assert new_job == response_data
    assert [] == errors


@pytest.mark.django_db
def test_04_retrieve_a_job(login, create_job):
    response = login.get(reverse('detail_job', kwargs={'pk': create_job['_id']}))
    response_data = response.data['data']
    errors = response.data['errors']
    print(create_job)
    [response_data.pop(x) for x in ['updated_at', 'created_at']]
    for item in ['start_date', 'end_date']:
        response_data[item] = datetime.fromtimestamp(int(response_data[item])).strftime('%Y-%m-%d')
        create_job[item] = datetime.fromtimestamp(int(create_job[item])).strftime('%Y-%m-%d')
    assert status.HTTP_200_OK == response.status_code
    assert create_job == response_data
    assert [] == errors


@pytest.mark.django_db
def test_05_update_a_job(login, create_job):
    new_job = generate_job_data('default')
    response = login.put(reverse('detail_job', kwargs={'pk': create_job['_id']}), new_job)
    response_data = response.data['data']
    errors = response.data['errors']
    new_job['_id'] = create_job['_id']
    [response_data.pop(x) for x in ['updated_at', 'created_at', 'is_active']]
    for item in ['start_date', 'end_date']:
        response_data[item] = datetime.fromtimestamp(int(response_data[item])).strftime('%Y-%m-%d')
        new_job[item] = new_job[item].strftime('%Y-%m-%d')
    assert status.HTTP_200_OK == response.status_code
    assert new_job == response_data
    assert [] == errors


@pytest.mark.django_db
def test_06_patch_a_job(login, create_job):
    response = login.patch(reverse('detail_job', kwargs={'pk': create_job['_id']}), dict(is_active=True))
    errors = response.data['errors']
    assert status.HTTP_200_OK == response.status_code
    assert response.data['data']['is_active']
    assert [] == errors


@pytest.mark.django_db
def test_07_delete_a_job(login, create_job):
    assert status.HTTP_204_NO_CONTENT == login.delete(reverse('detail_job', kwargs={'pk': create_job['_id']})).status_code


@pytest.mark.django_db
def test_08_delete_an_invalid_job(login):
    response = login.delete(reverse('detail_job', kwargs={'pk': '62b5d8db1952833dd22102dd'}))
    assert status.HTTP_404_NOT_FOUND == response.status_code
    assert {} == response.data['data']
    assert ['Information not found.'] == response.data['errors']


@pytest.mark.django_db
def test_09_get_all_job(login, create_job):
    response = login.get(reverse('list_create_job'))
    assert status.HTTP_200_OK == response.status_code
    assert response.data['data']
    assert [] == response.data['errors']
    assert response.data['total_jobs'] >= 1


@pytest.mark.django_db
def test_10_active_a_job_activated(login, create_job):
    response = login.patch(reverse('detail_job', kwargs={'pk': create_job['_id']}), dict())
    assert status.HTTP_400_BAD_REQUEST == response.status_code
    assert {} == response.data['data']
    assert ["The is active field must match."] == response.data['errors']


@pytest.mark.django_db
def test_11_end_date_is_less_than_start_date(login):
    new_job = generate_job_data('less')
    print(new_job)
    response = login.post(reverse('list_create_job'), new_job)
    assert status.HTTP_400_BAD_REQUEST == response.status_code
    assert {} == response.data['data']
    assert ["The end date field must not be less than the start date field."] == response.data['errors']
