import random

from ddt import ddt, data
from django.urls import reverse

from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from apps.tests_folder.UserTestsSetUp import RegisterUserTestSetUp, LoginUser


class PositiveUserRegistrationTestCases(RegisterUserTestSetUp):

    def test_01_register_a_new_user(self):
        self.assertEqual(self.resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.resp.data['data']['_id'])
        self.assertFalse(self.resp.data['errors'])


class NegativeUserRegistrationTestCases(APITestCase):
    register = RegisterUserTestSetUp()
    user: dict = {}

    def setUp(self) -> None:
        self.user = self.register._generate_user()

    def test_02_register_a_registered_user(self):
        self.client.post(reverse('user_create'), self.user)
        resp = self.client.post(reverse('user_create'), self.user)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ErrorDetail(resp.data['username'][0]).title(), 'User With This Username Already Exists.')
        self.assertEqual(ErrorDetail(resp.data['email'][0]).title(), 'User With This Email Already Exists.')

    def test_03_register_an_user_without_confirm_password(self):
        del self.user['confirm_password']
        resp = self.client.post(reverse('user_create'), self.user)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ErrorDetail(resp.data['confirm_password'][0]).title(), "This Field Is Required.")

    def test_04_validate_the_user_register_is_inactive(self):
        resp = self.client.post(reverse('user_create'), self.user)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertFalse(resp.data['data']['is_active'])
        self.assertFalse(resp.data['errors'])

    def test_05_validate_the_user_register_is_not_superuser(self):
        resp = self.client.post(reverse('user_create'), self.user)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertFalse(resp.data['data']['is_superuser'])
        self.assertFalse(resp.data['errors'])


class PositiveLoginTestCases(LoginUser):

    def test_01_valid_login(self):
        self.assertEqual(self.token.status_code, status.HTTP_200_OK)
        self.assertTrue(self.token.data['data'])
        self.assertTrue(self.token.data['data']['token'])
        self.assertTrue(self.token.data['data']['refresh'])
        self.assertTrue(self.token.data['data']['exp'])
        self.assertFalse(self.token.data['errors'])


@ddt
class NegativeLoginTestCases(RegisterUserTestSetUp):

    def test_01_attempt_make_login_without_active_the_new_user(self):
        resp = self.client.post(reverse('login'), self.credentials)
        self._error_assertions('forbidden', resp)

    @data('WP', 'WU', 'WORF')
    def test_02_with_wrong_field(self, action):
        match action:
            case 'WP':
                self.credentials['username'] = self.chance.first()
                resp = self.client.post(reverse('login'), self.credentials)
            case 'WU':
                self.credentials['password'] = self.chance.string()
                resp = self.client.post(reverse('login'), self.credentials)
            case _:
                self.credentials.pop(self.chance.pickone(['username', 'password']))
                resp = self.client.post(reverse('login'), self.credentials)

        self._error_assertions(resp=resp)


class GetAllUsersTestCasesUser(LoginUser):
    def test_01_validate_if_there_are_registered_users(self):
        how_much = random.randint(0, 100)
        for x in range(how_much):
            self.register()

        resp = self.client.get(reverse('all_users'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data['data'])
        self.assertFalse(resp.data['errors'])
        self.assertEqual(resp.data['total_users'], how_much + 1)


class DetailUserTestCasesUser(LoginUser):

    def test_01_get_one_user(self):
        user = self._adapt_user_to_validate(False)
        resp = self.client.get(reverse('user_detail', kwargs={'pk': user['_id']}))
        self._assertions_login_user('ok', resp, user)

    def test_02_updated_all_data_of_one_user(self):
        user = self._adapt_user_to_validate()
        resp = self.client.put(reverse('user_detail', kwargs={'pk': user['_id']}), user)
        [resp.data['data'].pop(x) for x in ['last_login', 'created_at', 'updated_at']]

        self._assertions_login_user('ok', resp, user)

    def test_03_update_one_thing_of_one_user(self):
        user = self._adapt_user_to_validate(False)
        resp = self.client.patch(reverse('user_detail', kwargs={'pk': user['_id']}), {'is_active': True})
        user['is_active'] = True
        [resp.data['data'].pop(x) for x in ['last_login', 'created_at', 'updated_at']]
        self._assertions_login_user('ok', resp, user)

    def test_04_delete_one_user(self):
        user = self._adapt_user_to_validate()
        resp = self.client.delete(reverse('user_detail', kwargs={'pk': user['_id']}))
        self._assertions_login_user(resp=resp, user=user)
        resp = self.client.get(reverse('user_detail', kwargs={'pk': user['_id']}))
        self._error_assertions('not_found', resp)


class ResetPasswordTestCasesUser(LoginUser):

    def setUp(self) -> None:
        super().setUp()
        self.data = self._generate_new_password()
        self.resp = self.client.patch(reverse('reset_password_of_user_logged'), self.data)

    def test_01_change_password(self):
        self.assertEqual(self.resp.status_code, status.HTTP_200_OK)
        self.assertEqual(self.resp.data['data'], 'Password updated successfully.')
        self.assertFalse(self.resp.data['errors'])

    def test_02_login_with_new_password(self):
        resp = self.client.post(reverse('login'), self.credentials)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data['data'])
        self.assertTrue(resp.data['data']['token'])
        self.assertFalse(resp.data['errors'])

    def test_03_attempt_to_login_with_changed_password(self):
        resp = self.client.post(reverse('login'), {'username': self.user['username'],
                                                   'password': self.user['password']})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.data['errors'][0], 'Invalid credentials.')


class NegativeResetPasswordTestCasesUser(LoginUser):

    def setUp(self) -> None:
        super().setUp()
        self.data = self._generate_new_password()
        self.fieldDeleted = self.chance.pickone(['old_password', 'new_password', 'confirm_password'])
        self.data.pop(self.fieldDeleted)
        self.resp = self.client.patch(reverse('reset_password_of_user_logged'), self.data)

    def test_01_attempt_change_password_without_required_field(self):
        self.assertEqual(self.resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ErrorDetail(self.resp.data[self.fieldDeleted][0]).title(), 'This Field Is Required.')
