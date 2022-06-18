from rest_framework import status


class Utilities(object):

    @staticmethod
    def bad_responses(response=str) -> list:
        data = {}
        match response:
            case 'not_found':
                return [{'data': data, 'errors': ['Information not found.']}, status.HTTP_404_NOT_FOUND]
            case 'information_recorded':
                return [{'data': data, 'errors': ['There is information recorded.']}, status.HTTP_406_NOT_ACCEPTABLE]
            case _:
                return [{'data': data, 'errors': ['Bad request.']}, status.HTTP_400_BAD_REQUEST]

    @staticmethod
    def ok_response(response=str, serializer=None) -> list:
        error = []
        match response:
            case 'post':
                return [{'data': serializer, 'errors': error}, status.HTTP_201_CREATED]
            case 'patch':
                return [{'data': {}, 'errors': error}, status.HTTP_204_NO_CONTENT]
            case _:
                return [{'data': serializer, 'errors': error}, status.HTTP_200_OK]
