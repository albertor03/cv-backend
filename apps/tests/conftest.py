import logging

import pytest
from rest_framework.reverse import reverse

from rest_framework.test import APIClient
from chance import chance

from apps.users.models import User
from apps.users.views import MakeToken


def generate_user_data():
    name = chance.first()
    last = chance.last()
    pwd = chance.string()
    return dict(
        username=f"{name}{last}".lower(),
        first_name=name,
        last_name=last,
        email=chance.email(),
        password=pwd,
        confirm_password=pwd
    )


@pytest.fixture()
def generate_user():
    return generate_user_data()


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def register(client, generate_user):
    payload = generate_user
    return client.post(reverse('user_create'), payload)


@pytest.fixture()
def user(client, generate_user):
    payload = generate_user
    user = User.objects.create_user(payload.get('username'), payload.get('email'), payload.get('first_name'),
                                    payload.get('last_name'), payload.get('password'))
    user.is_active = True
    user.save()

    return payload


@pytest.fixture()
def login(client, user):
    login = client.post(reverse('login'), user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['data']['token']}")
    return login


@pytest.fixture()
def generate_token(client, user):
    login_payload = dict(username=user['username'], password=user['password'])
    jwt = MakeToken().create_token(login_payload)
    user = User.objects.filter(username=user['username']).first()
    user.is_active = False
    user.save()
    return jwt