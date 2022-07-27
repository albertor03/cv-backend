from bson import ObjectId
from ddt import ddt, data
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from ..tests_folder.InformationSetUp import InformationSetUp


class PositiveUserRegistrationTestCasesUser(InformationSetUp):
    def test_01_register_new_information(self):
        self.assertEqual(self.resp.status_code, status.HTTP_201_CREATED)
        self._assertions()

    def test_02_list_information(self):
        resp = self._make_request('list')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self._assertions()


class NegativeUserRegistrationTestCasesUser(InformationSetUp):
    def test_01_register_an_information_registered(self):
        resp = self._make_request('create', self._generate_info())
        error = ErrorDetail(resp.data['errors'][0]).title()
        self.assertEqual(resp.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertFalse(resp.data['data'])
        self.assertEqual(error, 'There Is Information Recorded.')

    def test_02_register_an_information_without_required_fields(self):
        field_deleted = self.chance.pickone(['first_name', 'last_name', 'email', 'profession', 'about'])
        self.data.pop(field_deleted)
        resp = self._make_request('create', self.data)
        first = ErrorDetail(resp.data[field_deleted][0]).title()
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(first, 'This Field Is Required.')


class PositiveInformationTestCases(InformationSetUp):

    def test_01_update_information(self):
        _id = self.resp.data['data']['_id']
        self.data = self._generate_info()
        resp = self._make_request('put', self.data, _id)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data['data']['_id'], _id)
        self.assertEqual(resp.data['data']['first_name'], self.data['first_name'])
        self.assertEqual(resp.data['data']['last_name'], self.data['last_name'])
        self.assertEqual(resp.data['data']['email'], self.data['email'])
        self.assertEqual(resp.data['data']['profession'], self.data['profession'])

    def test_02_delete_information(self):
        resp = self._make_request('delete', _id=self.resp.data['data']['_id'])
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(resp.data)

    def test_03_empty_list(self):
        self._make_request('delete', _id=self.resp.data['data']['_id'])
        resp = self._make_request('info')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(resp.data)


@ddt
class NegativeInformationTestCases(InformationSetUp):
    @data('detail', 'put', 'patch', 'delete')
    def test_01_attempt_search_a_info_that_does_not_exist(self, action: str) -> None:
        info = self._generate_info()

        match action:
            case 'delete':
                self.resp = self._make_request(action, _id=ObjectId.from_datetime(self.date))
            case _:
                self.resp = self._make_request(action, info, ObjectId.from_datetime(self.date))

        self._assertions('404')
