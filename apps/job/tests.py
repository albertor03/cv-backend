import random

from datetime import datetime

from bson import ObjectId
from chance import chance
from ddt import ddt, data
from rest_framework import status

from ..tests_folder.JobTestsSetUp import TestJobSetUp


class PositiveCreateJobTest(TestJobSetUp):

    def test_01_create_a_new_job(self):
        self.assertEqual(self.resp.status_code, status.HTTP_201_CREATED)
        [self.resp.data['data'].pop(x) for x in ['_id', 'is_active']]
        for x in ['start_date', 'end_date']:
            self.resp.data['data'][x] = datetime.fromtimestamp(int(self.resp.data['data'][x])).strftime('%Y-%m-%d')
            self.data[x] = self.data[x].strftime('%Y-%m-%d')
        self.assertEqual(self.resp.data['data'], self.data)
        self.assertFalse(self.resp.data['errors'])

    def test_02_list_all_jobs(self):
        resp = self._make_request("list")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data['data'])
        self.assertFalse(resp.data['errors'])


class NegativeCreateJobTest(TestJobSetUp):
    def test_01_create_a_new_job_empty(self):
        resp = self._make_request("create", {})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(resp.data['data'])
        self.assertTrue(resp.data['errors'])

    def test_02_create_a_new_job_without_require_field(self):
        self.data.pop(self.chance.pickone(['position', 'company_name', 'start_date', 'address']))
        resp = self._make_request("create", self.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(resp.data['data'])
        self.assertEqual(resp.data['errors'][0], 'Bad request.')


class PositiveListRetrieveUpdateDestroyJobTest(TestJobSetUp):

    def test_01_get_a_job(self):
        resp = self._make_request("detail", _id=self.resp.data['data']['_id'])
        self._assertions(resp)

    def test_02_update_a_job(self):
        self.data = self._generate_job()
        resp = self._make_request('put', self.data, self.resp.data['data']['_id'])
        self._assertions(resp)

    def test_03_patch_a_job(self):
        is_active = chance.boolean()
        resp = self._make_request('patch', {'is_active': is_active}, self.resp.data['data']['_id'])
        self._assertions(resp)
        self.assertEqual(resp.data['data']['is_active'], is_active)

    def test_04_list_all_jobs(self):
        how = random.randint(1, 50)
        for x in range(how):
            self._generate_data()
        resp = self._make_request("list")
        self._assertions(resp)
        self.assertEqual(resp.data['total_jobs'], how + 1)

    def test_05_delete_job(self):
        resp = self._make_request('delete', _id=self.resp.data['data']['_id'])
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(resp.data)


@ddt
class NegativeJobTestCases(TestJobSetUp):
    @data('detail', 'put', 'patch', 'delete')
    def test_01_attempt_search_a_job_that_does_not_exist(self, action: str) -> None:
        job = self._generate_job()

        match action:
            case 'delete':
                resp = self._make_request(action, _id=ObjectId.from_datetime(self.date))
            case _:
                if action == 'patch':
                    job = {'is_active': self.chance.boolean()}
                resp = self._make_request(action, job, ObjectId.from_datetime(self.date))

        self._assertions(resp, '404')
