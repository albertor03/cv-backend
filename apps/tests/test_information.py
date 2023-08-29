from datetime import datetime

import pytest
from rest_framework import status

from rest_framework.reverse import reverse
from apps.information.models import PersonalInformationModel


@pytest.mark.django_db
def test_01_information_str(create_information):
    info = PersonalInformationModel.objects.filter(_id=create_information['_id']).first()
    assert f"{create_information['first_name']} {create_information['last_name']}" == info.__str__()
