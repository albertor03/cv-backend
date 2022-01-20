import random

from django.urls import reverse

from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from ..tests_folder.set_up import TestUserSetUp, RegistrationUser


class UserRegistrationTestCases(RegistrationUser):

    def setUp(self) -> None:
        self.register()

    def test_01_register_a_new_user(self):
        self.assertEqual(self.resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.resp.data['data']['_id'])
        self.assertFalse(self.resp.data['errors'])

    def test_02_register_a_registered_user(self):
        resp = self.client.post(reverse('user_create'), self.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        user = ErrorDetail(resp.data['username'][0]).title()
        email = ErrorDetail(resp.data['email'][0]).title()
        self.assertEqual(user, 'User With This Username Already Exists.')
        self.assertEqual(email, 'User With This Email Already Exists.')

    def test_03_register_an_user_without_confirm_password(self):
        self.data.pop('confirm_password')
        resp = self.client.post(reverse('user_create'), self.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ErrorDetail(resp.data['confirm_password'][0]).title(), "This Field Is Required.")

    def test_04_validate_the_user_register_is_inactive(self):
        self.assertEqual(self.resp.status_code, status.HTTP_201_CREATED)
        self.assertFalse(self.resp.data['data']['is_active'])
        self.assertFalse(self.resp.data['errors'])

    def test_05_validate_the_user_register_is_not_superuser(self):
        self.assertEqual(self.resp.status_code, status.HTTP_201_CREATED)
        self.assertFalse(self.resp.data['data']['is_superuser'])
        self.assertFalse(self.resp.data['errors'])


class GetAllUsersTestCasesUser(TestUserSetUp):
    def test_01_validate_if_there_are_registered_users(self):
        how_much = random.randint(0, 100)
        for x in range(how_much):
            self.client.post(reverse('user_create'), self.data)
            self.setUp()

        resp = self.client.get(reverse('all_users'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data['data'])
        self.assertFalse(resp.data['errors'])
        self.assertEqual(resp.data['total_user'], how_much + 1)


class DetailUserTestCasesUser(TestUserSetUp):
    def test_01_get_one_user(self):
        resp = self.client.get(reverse('user_detail', kwargs={'pk': self.resp.data['data']['_id']}))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data['data'])
        self.assertEqual(resp.data['data']['username'], self.data['username'])
        self.assertEqual(resp.data['data']['first_name'], self.data['first_name'])
        self.assertEqual(resp.data['data']['last_name'], self.data['last_name'])
        self.assertEqual(resp.data['data']['email'], self.data['email'])
        self.assertFalse(resp.data['errors'])

    def test_02_updated_all_data_of_one_user(self):
        self.data['is_active'] = True
        self.data['is_staff'] = True
        self.data['is_superuser'] = True
        self.data.pop('password')
        self.data.pop('confirm_password')

        resp = self.client.put(reverse('user_detail', kwargs={'pk': self.resp.data['data']['_id']}), self.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data['data'])
        self.assertEqual(resp.data['data']['username'], self.data['username'])
        self.assertEqual(resp.data['data']['first_name'], self.data['first_name'])
        self.assertEqual(resp.data['data']['last_name'], self.data['last_name'])
        self.assertEqual(resp.data['data']['email'], self.data['email'])
        self.assertTrue(resp.data['data']['is_active'])
        self.assertTrue(resp.data['data']['is_staff'])
        self.assertTrue(resp.data['data']['is_superuser'])
        self.assertFalse(resp.data['errors'])

    def test_03_update_one_thing_of_one_user(self):
        resp = self.client.patch(reverse('user_detail', kwargs={'pk': self.resp.data['data']['_id']}),
                                 {'is_active': True})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data['data'])
        self.assertEqual(resp.data['data']['username'], self.data['username'])
        self.assertEqual(resp.data['data']['first_name'], self.data['first_name'])
        self.assertEqual(resp.data['data']['last_name'], self.data['last_name'])
        self.assertEqual(resp.data['data']['email'], self.data['email'])
        self.assertTrue(resp.data['data']['is_active'])
        self.assertFalse(resp.data['data']['is_staff'])
        self.assertFalse(resp.data['data']['is_superuser'])
        self.assertFalse(resp.data['errors'])

    def test_04_delete_one_user(self):
        _id = self.resp.data['data']['_id']
        self.setUp()
        resp = self.client.delete(reverse('user_detail', kwargs={'pk': _id}))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(resp.data)
        resp = self.client.get(reverse('user_detail', kwargs={'pk': _id}))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(resp.data['data'])
        self.assertTrue(resp.data['errors'])
        self.assertEqual(resp.data['errors'][0], 'User not found.')
