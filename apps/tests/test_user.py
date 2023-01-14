import logging
import os

import pytest

from django.conf import settings

from chance import chance
from rest_framework.exceptions import ErrorDetail
from rest_framework.reverse import reverse

from apps.tests.conftest import generate_user_data
from apps.users.models import User
from apps.users.views import MakeToken


@pytest.mark.django_db
def test_register_user(client, register):
    response = register
    data = response.data['data']
    errors = response.data['errors']

    assert response.status_code == 201
    assert errors == []
    assert data['_id']


@pytest.mark.django_db
def test_failed_register_user(client, generate_user):
    payload = generate_user
    settings.EMAIL_REPLY = 121212
    response = client.post(reverse('user_create'), payload)
    settings.EMAIL_REPLY = [os.environ['EMAIL_REPLY']]
    data = response.data['data']
    errors = response.data['errors'][0]

    assert response.status_code == 424
    assert {} == data
    assert 'object is not iterable' in errors


@pytest.mark.django_db
def test_failed_register_user_with_different_passwords(client, generate_user):
    payload = generate_user
    payload['confirm_password'] = chance.string(length=8)
    response = client.post(reverse('user_create'), payload)
    data = response.data['data']
    errors = response.data['errors'][0]

    assert response.status_code == 400
    assert {} == data
    assert 'The passwords must match.' == ErrorDetail(errors)


@pytest.mark.django_db
def test_login_user(client, login):
    response = login
    assert response.status_code == 200
    response = response.data
    assert response['errors'] == []
    assert 'token' in response['data']
    assert 'refresh' in response['data']
    assert 'exp' in response['data']


@pytest.mark.django_db
def test_forbidden_login_user(client, generate_user):
    payload = generate_user
    client.post(reverse('user_create'), payload)

    response = client.post(reverse('login'), dict(username=payload['username'], password=payload['password']))
    assert response.status_code == 403
    response = response.data
    assert response['errors'] == ['Inactive user.']
    assert response['data'] == {}


@pytest.mark.django_db
def test_login_invalid_credentials(client, user):
    payload = user

    response = client.post(reverse('login'), dict(username=payload['username'], password='password'))
    assert response.status_code == 400
    response = response.data
    assert response['errors'] == ['Invalid credentials.']
    assert response['data'] == {}


@pytest.mark.django_db
def test_logout(client, login):
    response = client.get(reverse('logout'))
    assert response.status_code == 200
    assert response.data['errors'] == []
    assert response.data['data'] == 'Successfully logged out.'


@pytest.mark.django_db
def test_invalid_logout(client, user):
    client.post(reverse('login'), user)
    response = client.get(reverse('logout'))
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {'wwwwww'}")
    assert response.status_code == 401


@pytest.mark.django_db
def test_active_user(client, generate_token):
    jwt = generate_token
    response = client.patch(reverse('active_user', kwargs={'token': jwt['token']}))
    assert response.status_code == 200
    assert response.data['data'] == 'User active successfully.'
    assert response.data['errors'] == []


@pytest.mark.django_db
def test_active_activated_user(client, generate_token):
    jwt = generate_token
    client.patch(reverse('active_user', kwargs={'token': jwt['token']}))
    response = client.patch(reverse('active_user', kwargs={'token': jwt['token']}))
    assert response.status_code == 400
    assert response.data['data'] == ''
    assert response.data['errors'] == ['The user is already activated.']


@pytest.mark.django_db
def test_send_activate_link(client, login):
    resp = client.post(reverse('user_create'), generate_user_data())
    response = client.post(reverse('send-activate-user-link'), dict(username=resp.data['data']['username']))
    assert 200 == response.status_code
    assert 'User activation link sent successfully.' == response.data['data']
    assert [] == response.data['errors']


@pytest.mark.django_db
def test_send_activation_link_to_a_user_does_not_exist(client, login):
    response = client.post(reverse('send-activate-user-link'), dict(username=generate_user_data()['username']))
    assert 400 == response.status_code
    assert {} == response.data['data']
    assert 'User not exist.' == ErrorDetail(response.data['errors'][0])


@pytest.mark.django_db
def test_send_activation_link_to_an_activated_user(client, login):
    new_user = client.post(reverse('user_create'), generate_user_data()).data['data']
    user = User.objects.filter(username=new_user['username']).first()
    user.is_active = True
    user.save()

    response = client.post(reverse('send-activate-user-link'), dict(username=new_user['username']))
    assert 400 == response.status_code
    assert {} == response.data['data']
    assert 'The user is already activated.' == ErrorDetail(response.data['errors'][0])


@pytest.mark.django_db
def test_failed_send_activate_link(client, login):
    resp = client.post(reverse('user_create'), generate_user_data())
    settings.EMAIL_REPLY = 121212
    response = client.post(reverse('send-activate-user-link'), dict(username=resp.data['data']['username']))
    settings.EMAIL_REPLY = [os.environ['EMAIL_REPLY']]
    assert 424 == response.status_code
    assert '' == response.data['data']
    assert ['Something happened while sending the user activate email.'] == response.data['errors']


@pytest.mark.django_db
def test_get_all_user(client, login):
    response = client.get(reverse('all_users'))
    assert response.status_code == 200
    assert response.data['data'] != []
    assert response.data['errors'] == []
    assert response.data['total_users'] > 0


@pytest.mark.django_db
def test_get_a_user(client, login):
    _id = client.get(reverse('all_users')).data['data'][0]['_id']
    response = client.get(reverse('user_detail', kwargs={'pk': _id}))
    assert response.status_code == 200
    assert _id == response.data['data']['_id']
    assert response.data['errors'] == []


@pytest.mark.django_db
def test_get_a_user_do_not_exist(client, login):
    _id = '62b5d8db1952833dd22102dd'
    response = client.get(reverse('user_detail', kwargs={'pk': _id}))
    assert 404 == response.status_code
    assert {} == response.data['data']
    assert ["Information not found."] == response.data['errors']


@pytest.mark.django_db
def test_update_an_user(client, login):
    new_user = client.post(reverse('user_create'), generate_user_data()).data['data']
    _id = new_user['_id']
    new_user['is_active'] = True
    new_user['is_staff'] = True
    new_user['is_superuser'] = True
    new_user.pop('last_login')
    new_user.pop('created_at')
    new_user.pop('updated_at')
    new_user.pop('_id')
    response = client.put(reverse('user_detail', kwargs={'pk': _id}), new_user)
    assert response.status_code == 200
    assert _id == response.data['data']['_id']
    assert response.data['data']['is_active']
    assert response.data['data']['is_staff']
    assert response.data['data']['is_superuser']
    assert response.data['errors'] == []


@pytest.mark.django_db
def test_update_a_user_do_not_exist(client, login):
    new_user = client.post(reverse('user_create'), generate_user_data()).data['data']
    _id = '62b5d8db1952833dd22102dd'
    fields = ['username', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'created_at', 'updated_at']
    [new_user.pop(x) for x in fields]
    response = client.put(reverse('user_detail', kwargs={'pk': _id}), new_user)
    assert response.status_code == 404
    assert {} == response.data['data']
    assert ["Information not found."] == response.data['errors']


@pytest.mark.django_db
def test_update_a_user_without_required_field(client, login):
    new_user = client.post(reverse('user_create'), generate_user_data()).data['data']
    _id = new_user['_id']
    fields = ['username', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'created_at', 'updated_at']
    [new_user.pop(x) for x in fields]
    response = client.put(reverse('user_detail', kwargs={'pk': _id}), new_user)
    assert response.status_code == 400
    assert {} == response.data['data']
    assert ["Bad request."] == response.data['errors']


@pytest.mark.django_db
def test_patch_an_user(client, login):
    new_user = client.post(reverse('user_create'), generate_user_data()).data['data']
    _id = new_user['_id']
    new_email = generate_user_data()['email']
    response = client.patch(reverse('user_detail', kwargs={'pk': _id}), dict(email=new_email))
    assert 200 == response.status_code
    assert _id == response.data['data']['_id']
    assert new_email == response.data['data']['email']
    assert [] == response.data['errors']


@pytest.mark.django_db
def test_patch_a_user_do_not_exist(client, login):
    _id = '62b5d8db1952833dd22102dd'
    new_email = generate_user_data()['email']
    response = client.patch(reverse('user_detail', kwargs={'pk': _id}), dict(email=new_email))
    assert 404 == response.status_code
    assert {} == response.data['data']
    assert ["Information not found."] == response.data['errors']


@pytest.mark.django_db
def test_delete_an_user(client, login):
    new_user = client.post(reverse('user_create'), generate_user_data()).data['data']
    _id = new_user['_id']
    response = client.delete(reverse('user_detail', kwargs={'pk': _id}))
    assert 204 == response.status_code
    assert {} == response.data['data']
    assert [] == response.data['errors']


@pytest.mark.django_db
def test_delete_a_user_do_not_exist(client, login):
    response = client.delete(reverse('user_detail', kwargs={'pk': '62b5d8db1952833dd22102dd'}))
    assert 404 == response.status_code
    assert {} == response.data['data']
    assert ["Information not found."] == response.data['errors']


@pytest.mark.django_db
def test_update_user_password(client, user):
    old_pwd = chance.string(length=8)
    new_pwd = chance.string(length=8)
    jwt = MakeToken().create_token(dict(username=user['username'], password=user['password']))
    user_data = User.objects.filter(username=user['username']).first()
    user_data.set_password(old_pwd)
    user_data.save()
    payload = dict(old_password=old_pwd, new_password=new_pwd, confirm_password=new_pwd)

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt['token']}")
    response = client.patch(reverse('reset_password_of_user_logged'), payload, format='json')
    assert 200 == response.status_code
    assert 'Password updated successfully.' == response.data['data']
    assert [] == response.data['errors']


@pytest.mark.django_db
def test_update_password_with_an_invalid_old_password(client, user):
    old_pwd = chance.string(length=8)
    new_pwd = chance.string(length=8)
    jwt = MakeToken().create_token(dict(username=user['username'], password=user['password']))
    payload = dict(old_password=old_pwd, new_password=new_pwd, confirm_password=new_pwd)

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt['token']}")
    response = client.patch(reverse('reset_password_of_user_logged'), payload, format='json')
    assert 400 == response.status_code
    assert {} == response.data['data']
    assert 'The current password is not correct.' == ErrorDetail(response.data['errors'][0])


@pytest.mark.django_db
def test_update_password_with_mismatched_passwords(client, user):
    jwt = MakeToken().create_token(dict(username=user['username'], password=user['password']))
    payload = dict(old_password=user['password'], new_password=chance.string(length=8),
                   confirm_password=chance.string(length=8))

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt['token']}")
    response = client.patch(reverse('reset_password_of_user_logged'), payload, format='json')
    assert 400 == response.status_code
    assert {} == response.data['data']
    assert 'The passwords must match.' == ErrorDetail(response.data['errors'][0])


@pytest.mark.django_db
def test_send_reset_password_link(client, login):
    new_user = client.post(reverse('user_create'), generate_user_data()).data['data']
    user = User.objects.filter(username=new_user['username']).first()
    user.is_active = True
    user.save()
    response = client.patch(reverse('send-reset-password-link'), dict(username=new_user['username']))

    assert 200 == response.status_code
    assert 'Reset password link sent successfully.' == response.data['data']
    assert [] == response.data['errors']


@pytest.mark.django_db
def test_failed_send_password_reset_link(client, login):
    new_user = client.post(reverse('user_create'), generate_user_data()).data['data']
    user = User.objects.filter(username=new_user['username']).first()
    user.is_active = True
    user.save()
    settings.EMAIL_REPLY = 121212
    response = client.patch(reverse('send-reset-password-link'), dict(username=new_user['username']))
    settings.EMAIL_REPLY = [os.environ['EMAIL_REPLY']]

    assert 424 == response.status_code
    assert '' == response.data['data']
    assert ['Something happened while sending the user activate email.'] == response.data['errors']


@pytest.mark.django_db
def test_send_password_reset_link_to_non_existent_user(client, login):
    response = client.patch(reverse('send-reset-password-link'), dict(username=generate_user_data()['username']))

    assert 400 == response.status_code
    assert {} == response.data['data']
    assert 'User not exist.' == ErrorDetail(response.data['errors'][0])


@pytest.mark.django_db
def test_send_password_reset_link_to_inactive_user(client, login):
    new_user = client.post(reverse('user_create'), generate_user_data()).data['data']
    response = client.patch(reverse('send-reset-password-link'), dict(username=new_user['username']))

    assert 400 == response.status_code
    assert {} == response.data['data']
    assert 'The user is not activated.' == ErrorDetail(response.data['errors'][0])


@pytest.mark.django_db
def test_user_str_in_models(user):
    user_name = User.objects.filter(username=user['username']).first()
    assert f"{user['first_name']} {user['last_name']}" == user_name.__str__()


@pytest.mark.django_db
def test_user_natural_key_in_models(user):
    user_name = User.objects.filter(username=user['username']).first()
    assert user['username'] == user_name.natural_key()


@pytest.mark.django_db
def test_create_super_user(generate_user):
    user = generate_user
    super_user = User.objects.create_superuser(user['username'], user['email'], user['first_name'], user['last_name'],
                                               user['password'])
    assert super_user.is_superuser
