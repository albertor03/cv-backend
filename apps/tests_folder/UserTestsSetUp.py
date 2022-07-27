import random
import datetime

from bson import ObjectId
from chance import chance
from rest_framework import status

from rest_framework.test import APITestCase
from django.urls import reverse

from ..users.models import User


class RegisterUserTestSetUp(APITestCase):
    random = random
    chance = chance
    user = dict()
    superUser = dict()
    credentials = dict()
    date = str()
    resp = None

    def setUp(self) -> None:
        self.user = self.register()
        self.credentials = {'username': self.user['username'], 'password': self.user['password']}
        self.date = datetime.datetime(self.random.randint(2000, datetime.datetime.now().year),
                                      self.random.randint(1, 12), self.random.randint(1, 30))
        return super().setUp()

    def register(self):
        user = self._generate_user()
        self.resp = self.client.post(reverse('user_create'), user)
        return user

    def _error_assertions(self, what=str(), resp=None):
        match what:
            case 'forbidden':
                self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
                self.assertEqual(resp.data['errors'][0], 'Inactive user.')
            case 'not_found':
                self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
                self.assertFalse(resp.data['data'])
                self.assertTrue(resp.data['errors'])
                self.assertEqual(resp.data['errors'][0], 'Information not found.')
            case _:
                self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(resp.data['errors'][0], 'Invalid credentials.')

    def _generate_user(self) -> dict:
        name = self.chance.first()
        last = self.chance.last()
        pwd = self.chance.string()
        return {
            "username": f"{name}{last}",
            "first_name": name,
            "last_name": last,
            "email": self.chance.email(),
            "password": pwd,
            "confirm_password": pwd
        }


class LoginUser(RegisterUserTestSetUp):
    token = ''

    def setUp(self) -> None:
        super().setUp()
        self.login()

    def login(self):
        user = User.objects.filter(_id=ObjectId(self.resp.data['data']['_id'])).first()
        user.is_active = True
        user.save()
        self.token = self.client.post(reverse('login'), self.credentials)

        self.__authorize_user(self.token.data)

    def __authorize_user(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['data']['token']}")

    def _adapt_user_to_validate(self, is_active=True) -> dict:
        user = self.register()
        user['_id'] = self.resp.data['data']['_id']
        user['is_active'] = is_active
        user['is_staff'] = is_active
        user['is_superuser'] = is_active
        user.pop('password')
        user.pop('confirm_password')

        return user

    def _assertions_login_user(self, what=str(), resp=None, user=dict) -> None:
        match what:
            case 'ok':
                self.assertEqual(resp.status_code, status.HTTP_200_OK)
                self.assertEqual(resp.data['data'], user)
                self.assertFalse(resp.data['errors'])
            case _:
                self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
                self.assertFalse(resp.data)

    def _generate_new_password(self):
        old_pwd = self.user['password']
        self.credentials['password'] = self.chance.string()
        return {
            "old_password": old_pwd,
            "new_password": self.credentials['password'],
            "confirm_password": self.credentials['password']
        }
