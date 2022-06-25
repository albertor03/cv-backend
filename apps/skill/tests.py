import random

from chance import chance
from django.urls import reverse

from rest_framework import status
from ..tests_folder.set_up import TestUserSetUp, generate_skill


class ListCreateSkillTestCases(TestUserSetUp):

    def test_01_list_empty_skills(self):
        resp = self.client.get(reverse('list_create_skill'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertFalse(resp.data['data'])
        self.assertFalse(resp.data['errors'])

    def test_02_create_skill(self):
        skill = generate_skill()
        resp = self.client.post(reverse('list_create_skill'), skill)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['data']['name'], skill['name'])
        self.assertEqual(resp.data['data']['percentage'], skill['percentage'])
        self.assertFalse(resp.data['errors'])

    def test_03_list_skills(self):
        how = random.randint(1, 50)
        for x in range(how):
            self.client.post(reverse('list_create_skill'), generate_skill())

        resp = self.client.get(reverse('list_create_skill'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data['data'])
        self.assertFalse(resp.data['errors'])


class RetrieveUpdateDestroySkillTestCases(TestUserSetUp):

    def test_01_retrieve_skill(self):
        skill = generate_skill()
        resp = self.client.post(reverse('list_create_skill'), skill)
        resp = self.client.get(reverse('retrieve_update_destroy_skill', kwargs={'pk': resp.data['data']['_id']}))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['data']['name'], skill['name'])
        self.assertEqual(resp.data['data']['percentage'], skill['percentage'])
        self.assertFalse(resp.data['errors'])

    def test_02_update_a_skill(self):
        resp = self.client.post(reverse('list_create_skill'), generate_skill())
        skill = generate_skill()

        resp = self.client.put(reverse('retrieve_update_destroy_skill', kwargs={'pk': resp.data['data']['_id']}), skill)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['data']['name'], skill['name'])
        self.assertEqual(resp.data['data']['percentage'], skill['percentage'])
        self.assertFalse(resp.data['errors'])

    def test_03_path_a_skill(self):
        resp = self.client.post(reverse('list_create_skill'), generate_skill())
        skill = {'is_active': chance.boolean()}

        resp = self.client.patch(reverse('retrieve_update_destroy_skill', kwargs={'pk': resp.data['data']['_id']}),
                                 skill)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['data']['is_active'], skill['is_active'])
        self.assertFalse(resp.data['errors'])

    def test_04_delete_a_skill(self):
        resp = self.client.post(reverse('list_create_skill'), generate_skill())
        resp = self.client.delete(reverse('retrieve_update_destroy_skill', kwargs={'pk': resp.data['data']['_id']}))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(resp.data)
