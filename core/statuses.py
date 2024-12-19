from rest_framework import status

BAD_REQUEST_400 = {
    'detail': 'Bad request',
    'code': 'bad_request',
    'number': status.HTTP_400_BAD_REQUEST
}

OK_200 = {
    'detail': 'Success',
    'code': 'success',
    'number': status.HTTP_200_OK
}

INTERNAL_SERVER_ERROR_500 = {
    'detail': 'Internal server error',
    'code': 'internal_server_error',
    'number': status.HTTP_500_INTERNAL_SERVER_ERROR
}