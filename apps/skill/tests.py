from bson import ObjectId
from ddt import ddt, data

from django.urls import reverse

from ..tests_folder.SkillTestsSetUp import SkillTests


class PositiveSkillTestCases(SkillTests):

    def test_01_list_empty_skills(self):
        resp = self._skill_request()
        self.assertEqual(resp.status_code, self.status.HTTP_200_OK)
        self.assertFalse(resp.data['data'])
        self.assertFalse(resp.data['errors'])

    def test_02_create_skill(self):
        resp = self._skill_request('post')
        self.assertEqual(resp.status_code, self.status.HTTP_201_CREATED)
        self._assertions(resp=resp)

    def test_03_list_skills(self):
        how = self.random.randint(1, 50)
        for x in range(how):
            self._skill_request('post')

        resp = self._skill_request()
        self.assertEqual(resp.status_code, self.status.HTTP_200_OK)
        self.assertTrue(resp.data['data'])
        self.assertFalse(resp.data['errors'])

    def test_04_retrieve_skill(self):
        resp = self._skill_request('post')
        resp = self.client.get(reverse('retrieve_update_destroy_skill', kwargs={'pk': resp.data['data']['_id']}))
        self.assertEqual(resp.status_code, self.status.HTTP_200_OK)
        self._assertions(resp=resp)

    def test_05_update_a_skill(self):
        resp = self._skill_request('post')
        resp = self.client.put(reverse('retrieve_update_destroy_skill', kwargs={'pk': resp.data['data']['_id']}),
                               self.skill)
        self.assertEqual(resp.status_code, self.status.HTTP_200_OK)
        self._assertions(resp=resp)

    def test_06_path_a_skill(self):
        resp = self._skill_request('post')
        skill = {'is_active': self.chance.boolean()}

        resp = self.client.patch(reverse('retrieve_update_destroy_skill', kwargs={'pk': resp.data['data']['_id']}),
                                 skill)
        self.assertEqual(resp.status_code, self.status.HTTP_200_OK)
        self.assertEqual(resp.data['data']['is_active'], skill['is_active'])
        self.assertFalse(resp.data['errors'])

    def test_07_delete_a_skill(self):
        resp = self._skill_request('post')
        resp = self.client.delete(reverse('retrieve_update_destroy_skill', kwargs={'pk': resp.data['data']['_id']}))
        self.assertEqual(resp.status_code, self.status.HTTP_204_NO_CONTENT)
        self.assertFalse(resp.data)


@ddt
class NegativeSkillTestCases(SkillTests):

    def test_01_attempt_create_a_skill_without_required_field(self):
        self.skill.pop(self.chance.pickone(['name', 'percentage']))
        resp = self._skill_request('post')
        self._assertions('bad', resp)

    @data('get', 'update', 'patch', 'delete')
    def test_02_attempt_search_a_skill_that_does_not_exist(self, action):
        match action:
            case 'get':
                resp = self.client.get(reverse('retrieve_update_destroy_skill',
                                               kwargs={'pk': ObjectId.from_datetime(self.date)}),
                                       self.skill)
            case 'update':
                resp = self.client.put(reverse('retrieve_update_destroy_skill',
                                               kwargs={'pk': ObjectId.from_datetime(self.date)}),
                                       self.skill)
            case 'patch':
                skill = {'is_active': self.chance.boolean()}
                resp = self.client.patch(reverse('retrieve_update_destroy_skill',
                                                 kwargs={'pk': ObjectId.from_datetime(self.date)}),
                                         skill)
            case _:
                resp = self.client.delete(reverse('retrieve_update_destroy_skill',
                                                  kwargs={'pk': ObjectId.from_datetime(self.date)}))

        self._assertions('404', resp)
