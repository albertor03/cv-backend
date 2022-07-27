from datetime import datetime
import random

from bson import ObjectId
from chance import chance

from django.urls import reverse

from rest_framework.test import APITestCase

from ..users.models import User


def generate_job():
    return {
        "position": chance.string(),
        "company_name": chance.string(),
        "start_date": datetime.now(),
        "end_date": datetime.now(),
        "currently": chance.boolean(),
        "address": chance.country(),
        "description": chance.paragraph(1)
    }


def generate_data():
    name = chance.name()
    last = chance.last()
    return {
        "first_name": name,
        "last_name": last,
        "email": chance.email(),
        "profession": "Professional Testing",
        "phone": chance.phone(formatted=False),
        "address": chance.city(),
        "about": chance.paragraph(1)
    }


class TestInformationSetUp(LoginUser):

    def setUp(self) -> None:
        self.login()
        self.data = generate_data()
        self.resp = self.client.post(reverse('info'), self.data)


class TestJobSetUp(LoginUser):

    def setUp(self) -> None:
        self.login()
        self.data = generate_job()
        self.resp = self.client.post(reverse('list_create_job'), self.data)

