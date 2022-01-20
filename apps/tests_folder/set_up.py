from bson import ObjectId
from faker import Faker

from django.urls import reverse

from rest_framework.test import APITestCase

from ..users.models import User


def generate_user():
    name = str(Faker().name())
    return {
        "username": name.lower().replace(' ', ''),
        "first_name": name.split(' ')[0],
        "last_name": name.split(' ')[1],
        "email": f"{name.lower().replace(' ', '')}@mailinator.com",
        "password": "Cenpos*01",
        "confirm_password": "Cenpos*01"
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
        self.data = self.generate_data()
        self.resp = self.client.post(reverse('info'), self.data)

    @staticmethod
    def generate_data():
        name = str(Faker().name())
        return {
            "first_name": name.split(' ')[0],
            "last_name": name.split(' ')[1],
            "email": f"{name.lower().replace(' ', '')}@mailinator.com",
            "profession": "Professional Testing",
            "phone": "123456789",
            "address": Faker().address()
        }
