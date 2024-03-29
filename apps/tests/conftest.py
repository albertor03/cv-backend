import base64
import datetime
import random

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


def generate_skill_data():
    return dict(
        name=chance.string(length=10),
        percentage=float(f"{random.randint(0, 100)}.{random.randint(0, 99)}"),
        is_active=False
    )


def generate_job_data(data_type):
    data = dict(
        position=chance.string(length=10),
        company_name=chance.string(length=10),
        start_date=datetime.datetime.now() - datetime.timedelta(days=60),
        end_date=datetime.datetime.now() - datetime.timedelta(days=30),
        currently=chance.pickone([True, False]),
        address=chance.city(),
        description=chance.string(length=150),
    )
    match data_type:
        case "end":
            data.pop("currently")
        case 'currently':
            data.pop("end_date")
        case "without":
            data.pop("currently")
            data.pop("end_date")
        case 'active':
            data['is_active'] = True
        case 'less':
            data['end_date'] -= datetime.timedelta(days=60)

    return data


def generate_info_data():
    social = dict(
                name=chance.string(pool='abcdef8', minimum=5, maximum=20),
                link=chance.url(exts=[".com"])
            )
    return dict(
        first_name=chance.first(),
        last_name=chance.last(),
        profession=chance.string(pool='abcdef8', minimum=5, maximum=20),
        about=chance.paragraph(sentences=1),
        profile_photo=chance.filepath(),
        contact_info=dict(
            email=chance.email(),
            phone=chance.phone(formatted=False),
            address=chance.country()
        ),
        contact_social=[social]
    )


def generate_education_data(data_type='default'):
    start_date = datetime.datetime.now() - datetime.timedelta(days=60)
    end_date = datetime.datetime.now() - datetime.timedelta(days=30)
    data = dict(
        degree=chance.string(length=10),
        collage=chance.string(length=10),
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=end_date.strftime("%Y-%m-%d"),
        currently=chance.pickone([True, False]),
        certificate=base64.b64encode(chance.string(length=10).encode()).decode('utf-8'),
        is_active=chance.pickone([True, False])
    )
    match data_type:
        case 'base64':
            data['certificate'] = "Hola esto es una prueba"
        case 'less':
            date = datetime.datetime.now() - datetime.timedelta(days=100)
            data['end_date'] = date.strftime("%Y-%m-%d")
    return data


def generate_course_data(data_type="base64"):
    if data_type == "base64":
        certificate = base64.b64encode(chance.string(length=10).encode()).decode('utf-8')
    else:
        certificate = chance.string(length=10)

    return dict(
        name=chance.string(length=10),
        company=chance.string(length=10),
        end_date=datetime.datetime.now().strftime("%Y-%m-%d"),
        certificate=certificate,
        is_active=chance.pickone([True, False])
    )


def generate_course_section_data(data_type='default'):
    data = dict(
        name=chance.string(length=10),
        courses=[],
    )

    match data_type:
        case 'with':
            data['courses'].append(generate_course_data())
    return data


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
def user(generate_user):
    payload = generate_user
    user = User.objects.create_user(payload.get('username'), payload.get('email'), payload.get('first_name'),
                                    payload.get('last_name'), payload.get('password'))
    user.is_active = True
    user.save()

    return payload


@pytest.fixture()
def login(client, user):
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {client.post(reverse('login'), user).data['data']['token']}")
    return client


@pytest.fixture()
def generate_token(client, user):
    login_payload = dict(username=user['username'], password=user['password'])
    jwt = MakeToken().create_token(login_payload)
    user = User.objects.filter(username=user['username']).first()
    user.is_active = False
    user.save()
    return jwt


@pytest.fixture()
def create_skill(login):
    return login.post(reverse('list_create_skill'), generate_skill_data()).data['data']


@pytest.fixture()
def create_job(login):
    return login.post(reverse('list_create_job'), generate_job_data("default")).data['data']


@pytest.fixture()
def create_information(login):
    return login.post(reverse('info'), generate_info_data(), format='json').data['data']


@pytest.fixture()
def create_education(login):
    return login.post(reverse('list_create_education'), generate_education_data(), format='json').data['data']


@pytest.fixture()
def create_course_section(login):
    return login.post(reverse('list_create_course_section'), generate_course_section_data(), format='json').data['data']


@pytest.fixture()
def create_course(login, create_course_section):
    course_section_id = create_course_section['_id']
    course_data = generate_course_data()
    course_data['course_section_id'] = course_section_id
    return login.post(reverse('list_create_course'), course_data, format='json').data['data']
