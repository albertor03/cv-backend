import random

from chance import chance
from django.urls import reverse
from rest_framework import status

from ..tests_folder.set_up import TestJobSetUp, LoginUser, generate_job


class CreateJobTest(LoginUser):

    def setUp(self) -> None:
        self.login()

    def test_01_create_a_new_job_empty(self):
        resp = self.client.post(reverse('list_create_job'), {})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(resp.data['data'])
        self.assertTrue(resp.data['errors'])

    def test_02_create_a_new_job_without_require_field(self):
        data = generate_job()
        data.pop('position')
        resp = self.client.post(reverse('list_create_job'), data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(resp.data['data'])
        self.assertTrue(resp.data['errors'])

    def test_03_create_a_new_job(self):
        data = generate_job()
        resp = self.client.post(reverse('list_create_job'), data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(resp.data['data'])
        self.assertFalse(resp.data['errors'])


class ListRetrieveUpdateDestroyJobTest(TestJobSetUp):

    def test_01_get_a_job(self):
        _id = self.resp.data['data']['_id']

        resp = self.client.get(reverse('detail_job', kwargs={'pk': _id}))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data['data'])
        self.assertFalse(resp.data['errors'])
        self.assertEqual(resp.data['data']['position'], self.data['position'])

    def test_02_update_a_job(self):
        _id = self.resp.data['data']['_id']
        self.setUp()
        resp = self.client.put(reverse('detail_job', kwargs={'pk': _id}), self.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data['data'])
        self.assertFalse(resp.data['errors'])
        self.assertEqual(resp.data['data']['position'], self.data['position'])

    def test_03_patch_a_job(self):
        _id = self.resp.data['data']['_id']
        position = chance.string()
        resp = self.client.patch(reverse('detail_job', kwargs={'pk': _id}), {'position': position})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data['data'])
        self.assertFalse(resp.data['errors'])
        self.assertEqual(resp.data['data']['position'], position)

    def test_04_patch_a_job(self):
        how = random.randint(1, 50)
        for x in range(how):
            self.setUp()
        resp = self.client.get(reverse('list_create_job'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data['data'])
        self.assertFalse(resp.data['errors'])
        self.assertEqual(resp.data['total_user'], how + 1)

    def test_05_delete_job(self):
        _id = self.resp.data['data']['_id']
        resp = self.client.delete(reverse('detail_job', kwargs={'pk': _id}))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(resp.data)

