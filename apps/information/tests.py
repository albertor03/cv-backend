from django.urls import reverse

from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from ..tests_folder.set_up import TestInformationSetUp, Faker, LoginUser


class UserRegistrationTestCasesUser(TestInformationSetUp):
    def test_01_register_new_information(self):
        self.assertEqual(self.resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.resp.data['data']['_id'])
        self.assertFalse(self.resp.data['errors'])

    def test_02_register_an_information_registered(self):
        resp = self.client.post(reverse('info'), self.data)
        error = ErrorDetail(resp.data['errors'][0]).title()
        self.assertEqual(resp.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertFalse(resp.data['data'])
        self.assertEqual(error, 'There Is Information Recorded.')

    def test_03_register_an_information_without_required_fields(self):
        data = {
            "phone": "123456789",
            "address": Faker().address()
        }
        resp = self.client.post(reverse('info'), data)
        first = ErrorDetail(resp.data['first_name'][0]).title()
        last = ErrorDetail(resp.data['last_name'][0]).title()
        email = ErrorDetail(resp.data['email'][0]).title()
        profession = ErrorDetail(resp.data['profession'][0]).title()
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(first, 'This Field Is Required.')
        self.assertEqual(last, 'This Field Is Required.')
        self.assertEqual(email, 'This Field Is Required.')
        self.assertEqual(profession, 'This Field Is Required.')


class UserListTestCasesUser(LoginUser):

    def setUp(self) -> None:
        self.login()

    def test_01_empty_list(self):
        resp = self.client.get(reverse('info'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertFalse(resp.data)

    def test_02_list_information(self):
        name = str(Faker().name())
        data = {
            "first_name": name.split(' ')[0],
            "last_name": name.split(' ')[1],
            "email": f"{name.lower().replace(' ', '')}@mailinator.com",
            "profession": "Professional Testing",
            "phone": "123456789",
            "address": Faker().address()
        }
        self.client.post(reverse('info'), data)
        resp = self.client.get(reverse('info'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data)
        self.assertTrue(resp.data[0]['_id'])
        self.assertEqual(len(resp.data), 1)


class UserDetailTestCasesUser(TestInformationSetUp):

    def test_01_retrieve_information(self):
        _id = self.resp.data['data']['_id']

        resp = self.client.get(reverse('info_detail', kwargs={'pk': _id}))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data['data']['_id'], _id)
        self.assertEqual(resp.data['data']['first_name'], self.resp.data['data']['first_name'])
        self.assertEqual(resp.data['data']['last_name'], self.resp.data['data']['last_name'])
        self.assertEqual(resp.data['data']['email'], self.resp.data['data']['email'])
        self.assertEqual(resp.data['data']['profession'], self.resp.data['data']['profession'])

    def test_02_update_information(self):
        _id = self.resp.data['data']['_id']
        self.setUp()

        resp = self.client.put(reverse('info_detail', kwargs={'pk': _id}), self.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data['data']['_id'], _id)
        self.assertEqual(resp.data['data']['first_name'], self.data['first_name'])
        self.assertEqual(resp.data['data']['last_name'], self.data['last_name'])
        self.assertEqual(resp.data['data']['email'], self.data['email'])
        self.assertEqual(resp.data['data']['profession'], self.data['profession'])

    def test_03_delete_information(self):
        resp = self.client.delete(reverse('info_detail', kwargs={'pk': self.resp.data['data']['_id']}))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(resp.data)
