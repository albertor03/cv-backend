from rest_framework import status


class Utilities(object):

    @staticmethod
    def bad_responses(response="") -> list:
        switch = {
            'not_found': [{'data': {}, 'errors': ['Information not found.']}, status.HTTP_404_NOT_FOUND],
            'bad_request': [{'data': {}, 'errors': ['Bad request.']}, status.HTTP_400_BAD_REQUEST],
            'information_recorded': [{'data': {}, 'errors': ['There is information recorded.']},
                                     status.HTTP_406_NOT_ACCEPTABLE]
        }

        return switch.get(response, 'bad_request')

    @staticmethod
    def ok_response(response, serializer) -> list:
        switch = {
            'ok': [{'data': serializer, 'errors': []}, status.HTTP_200_OK],
            'post': [{'data': serializer, 'errors': []}, status.HTTP_201_CREATED],
            'patch': [{'data': {}, 'errors': []}, status.HTTP_204_NO_CONTENT]
        }

        return switch.get(response, 'ok')
