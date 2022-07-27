import datetime

from bson import ObjectId
from django.urls import reverse
from rest_framework import status

from .UserTestsSetUp import LoginUser


class TestJobSetUp(LoginUser):
    skill = dict()
    status = status
    date = str()

    def setUp(self) -> None:
        super().setUp()
        self._generate_data()
        self.date = datetime.datetime(self.random.randint(2000, datetime.datetime.now().year),
                                      self.random.randint(1, 12), self.random.randint(1, 30))

    def _generate_data(self):
        self.data: TestJobSetUp._generate_job = self._generate_job()
        self.resp = self._make_request("create", self.data)

    def _generate_job(self) -> dict:
        return {
            "position": self.chance.string(),
            "company_name": self.chance.string(),
            "start_date": datetime.datetime.now(),
            "end_date": datetime.datetime.now(),
            "currently": self.chance.boolean(),
            "address": self.chance.country(),
            "description": self.chance.paragraph(1)
        }

    def _assertions(self, resp, action="generic"):
        if action == "generic":
            self.assertEqual(resp.status_code, self.status.HTTP_200_OK)
            self.assertTrue(resp.data['data'])
            self.assertFalse(resp.data['errors'])
            if len(resp.data['data']) <= 1:
                self.assertEqual(resp.data['data']['position'], self.data['position'])
        else:
            self.assertEqual(resp.status_code, self.status.HTTP_404_NOT_FOUND)
            self.assertEqual(resp.data['errors'][0], 'Information not found.')

    def _make_request(self, request: str, data=_generate_job, _id=ObjectId):
        match request:
            case "create":
                return self.client.post(reverse('list_create_job'), data)
            case "detail":
                return self.client.get(reverse('detail_job', kwargs={'pk': _id}))
            case "put":
                return self.client.put(reverse('detail_job', kwargs={'pk': _id}), data)
            case "patch":
                return self.client.patch(reverse('detail_job', kwargs={'pk': _id}), data)
            case "delete":
                return self.client.delete(reverse('detail_job', kwargs={'pk': _id}))
            case _:
                return self.client.get(reverse('list_create_job'))
