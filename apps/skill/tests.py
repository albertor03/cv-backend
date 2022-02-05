from django.urls import reverse

from rest_framework import status
from ..tests_folder.set_up import TestUserSetUp, generate_skill


class CreateSkillTestCases(TestUserSetUp):
    def test_01_create_skill(self):
        skill = generate_skill()
        resp = self.client.post(reverse('list_create_skill'), skill)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['data']['name'], skill['name'])
        self.assertEqual(resp.data['data']['percentage'], skill['percentage'])
        self.assertFalse(resp.data['errors'])
