from rest_framework import status


class Utilities(object):

    @staticmethod
    def return_response(response="") -> list:
        switch = {
            'not_found': [{'data': {}, 'errors': ['Information not found.']}, status.HTTP_404_NOT_FOUND],
            'bad_request': [{'data': {}, 'errors': ['Bad request.']}, status.HTTP_400_BAD_REQUEST],
            'information_recorded': [{'data': {}, 'errors': ['There is information recorded.']},
                                     status.HTTP_406_NOT_ACCEPTABLE]
        }

        return switch.get(response, 'bad_request')
