from datetime import datetime
import random

from bson import ObjectId
from chance import chance

from django.urls import reverse

from rest_framework.test import APITestCase

from ..users.models import User


def generate_user():
    name = chance.first()
    last = chance.last()
    pwd = chance.string()
    return {
        "username": f"{name}{last}",
        "first_name": name,
        "last_name": last,
        "email": "alberto.zapata.orta@gmail.com",
        "password": pwd,
        "confirm_password": pwd
    }


def generate_job():
    return {
        "position": chance.string(),
        "company_name": chance.string(),
        "start_date": datetime.now(),
        "end_date": datetime.now(),
        "currently": chance.boolean(),
        "address": chance.country()
    }


def generate_data():
    name = chance.name()
    last = chance.last()
    return {
        "first_name": name,
        "last_name": last,
        "email": f"{name}{last}@mailinator.com",
        "profession": "Professional Testing",
        "phone": chance.phone(),
        "address": chance.city()
    }


def generate_skill():
    return {
        "name": f"{chance.name()} Skill",
        "percentage": random.uniform(0.0, 100.00)
    }


class RegistrationUser(APITestCase):
    data = dict()
    resp = None

    def register(self):
        self.data = generate_user()
        self.resp = self.client.post(reverse('user_create'), self.data)


class LoginUser(APITestCase):
    data = dict()
    resp = None

    def login(self):
        self.data = generate_user()
        self.resp = self.client.post(reverse('user_create'), self.data)
        user = User.objects.filter(_id=ObjectId(self.resp.data['data']['_id'])).first()
        user.is_active = True
        user.save()
        token = self.client.post(reverse('login'),
                                 {'username': self.data['username'], "password": self.data['password']}).data

        self.__authorize_user(token)

    def __authorize_user(self, token):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token['data']['token'])


class TestUserSetUp(LoginUser):

    def setUp(self) -> None:
        self.login()


class TestInformationSetUp(LoginUser):

    def setUp(self) -> None:
        self.login()
        self.data = generate_data()
        self.resp = self.client.post(reverse('info'), self.data)


class TestJobSetUp(LoginUser):

    def setUp(self) -> None:
        self.login()
        self.data = generate_job()
        self.resp = self.client.post(reverse('list_create_job'), self.data)


class TestChangePwdSetUp(LoginUser):
    newPwd = chance.string()
    oldPwd = ""
    originUser = ""

    def setUp(self) -> None:
        self.login()
        self.oldPwd = self.data['password']
        self.originUser = self.data['username']
        self.data = {
            "old_password": self.oldPwd,
            "new_password": self.newPwd,
            "confirm_password": self.newPwd
        }
        self.resp = self.client.patch(reverse('reset_password_of_user_logged'), self.data)
