from django.urls import reverse
from rest_framework import status

from apps.tests_folder.UserTestsSetUp import LoginUser


class SkillTests(LoginUser):
    skill = dict()
    status = status

    def setUp(self) -> None:
        super().setUp()
        self.skill = self.__generate_skill()

    def _skill_request(self, request=str()):
        match request:
            case 'post':
                return self.client.post(reverse('list_create_skill'), self.skill)
            case _:
                return self.client.get(reverse('list_create_skill'))

    def __generate_skill(self) -> dict:
        return {
            "name": f"{self.chance.name()} Skill",
            "percentage": self.random.uniform(0.0, 100.00),
            "is_active": self.chance.boolean()
        }

    def _assertions(self, what=str(), resp=None) -> None:
        match what:
            case 'bad':
                self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(resp.data['errors'][0], 'Bad request.')
            case '404':
                self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
                self.assertEqual(resp.data['errors'][0], 'Information not found.')
            case _:
                self.assertEqual(resp.data['data']['name'], self.skill['name'])
                self.assertEqual(resp.data['data']['percentage'], self.skill['percentage'])
                self.assertEqual(resp.data['data']['is_active'], self.skill['is_active'])
                self.assertFalse(resp.data['errors'])
