import pytest

from rest_framework.reverse import reverse

from apps.skill.models import SkillModel
from apps.tests.conftest import generate_skill_data


@pytest.mark.django_db
def test_get_all_skill(login):
    response = login.get(reverse('list_create_skill'))
    errors = response.data['errors']

    assert 200 == response.status_code
    assert [] == errors
    assert 0 <= response.data['total_skills']


@pytest.mark.django_db
def test_create_a_skill(login):
    skill = generate_skill_data()
    response = login.post(reverse('list_create_skill'), skill)
    data = response.data['data']
    errors = response.data['errors']

    assert 201 == response.status_code
    assert [] == errors
    assert skill['name'] == data['name']
    assert skill['percentage'] == data['percentage']
    assert 'total_skills' not in data


@pytest.mark.django_db
def test_get_a_skill(login, create_skill):
    response = login.get(reverse('retrieve_update_destroy_skill', kwargs={'pk': create_skill['_id']}))
    data = response.data['data']
    errors = response.data['errors']

    assert 200 == response.status_code
    assert [] == errors
    assert create_skill['_id'] == data['_id']
    assert create_skill['percentage'] == data['percentage']


@pytest.mark.django_db
def test_update_a_skill(login, create_skill):
    new_skill = generate_skill_data()
    response = login.put(reverse('retrieve_update_destroy_skill', kwargs={'pk': create_skill['_id']}), new_skill)
    data = response.data['data']
    errors = response.data['errors']

    assert 200 == response.status_code
    assert [] == errors
    assert new_skill['name'] == data['name']
    assert new_skill['percentage'] == data['percentage']


@pytest.mark.django_db
def test_patch_a_skill(login, create_skill):
    response = login.patch(reverse('retrieve_update_destroy_skill', kwargs={'pk': create_skill['_id']}),
                           dict(is_active=True))
    data = response.data['data']
    errors = response.data['errors']

    assert 200 == response.status_code
    assert [] == errors
    assert create_skill['name'] == data['name']
    assert create_skill['percentage'] == data['percentage']
    assert data['is_active']


@pytest.mark.django_db
def test_delete_a_skill(login, create_skill):
    assert 204 == login.delete(reverse('retrieve_update_destroy_skill', kwargs={'pk': create_skill['_id']})).status_code


@pytest.mark.django_db
def test_delete_a_non_exist_skill(login):
    response = login.delete(reverse('retrieve_update_destroy_skill', kwargs={'pk': '62b5d8db1952833dd22102dd'}))
    assert 404 == response.status_code
    assert {} == response.data['data']
    assert ['Information not found.'] == response.data['errors']


@pytest.mark.django_db
def test_skill_str(create_skill):
    skill_name = SkillModel.objects.filter(name=create_skill['name']).first()
    assert f"{create_skill['name']} about {create_skill['percentage']}" == skill_name.__str__()
