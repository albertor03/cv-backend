from bson import ObjectId
from django.urls import reverse

from .UserTestsSetUp import LoginUser


class InformationSetUp(LoginUser):

    def setUp(self) -> None:
        super().setUp()
        self.data = self._generate_info()
        self.resp = self._make_request("create", self.data)

    def _generate_info(self) -> dict:
        return {
            "first_name": self.chance.name(),
            "last_name": self.chance.last(),
            "email": self.chance.email(),
            "profession": "Professional Testing",
            "phone": self.chance.phone(formatted=False),
            "address": self.chance.city(),
            "about": self.chance.paragraph(1)
        }

    def _make_request(self, request, data=_generate_info, _id=ObjectId):
        match request:
            case "put":
                return self.client.put(reverse('info_detail', kwargs={'pk': _id}), data)
            case "create":
                return self.client.post(reverse('info'), data)
            case "delete":
                return self.client.delete(reverse('info_detail', kwargs={'pk': _id}))
            case _:
                return self.client.get(reverse('info'))

    def _assertions(self, assertion="ok") -> None:
        if assertion == "ok":
            self.assertTrue(self.resp.data['data']['_id'])
            self.assertFalse(self.resp.data['errors'])
