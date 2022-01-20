from bson import ObjectId

from ..models import User
from django.urls import reverse
from faker import Faker
from rest_framework.test import APITestCase


class TestSetUp(APITestCase):

    def setUp(self) -> None:
        self.data = self.generate_data()
        self.resp = self.client.post(reverse('user_create'), self.data).data
        user = User.objects.filter(_id=ObjectId(self.resp['data']['_id'])).first()
        user.is_active = True
        user.save()
        token = self.client.post(reverse('login'),
                                 {'username': self.data['username'], "password": self.data['password']}).data
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token['data']['token'])

    @staticmethod
    def generate_data():
        name = str(Faker().name())
        return {
            "username": name.lower().replace(' ', ''),
            "first_name": name.split(' ')[0],
            "last_name": name.split(' ')[1],
            "email": f"{name.lower().replace(' ', '')}@mailinator.com",
            "password": "Cenpos*01",
            "confirm_password": "Cenpos*01"
        }
