# apps/api/responses.py

from rest_framework.response import Response
from .statuses import OK_200, BAD_REQUEST_400, INTERNAL_SERVER_ERROR_500

def custom_response(status_code: dict = OK_200, data: dict or list = None, error=None):
    return Response(
        data={
            'detail': status_code.get('detail'),
            'code': status_code.get('code', status_code.get('detail').replace(' ', '_')),
            'error': error,
            'data': data if data else {}
        },
        status=status_code.get('number')
    )

def bad_request_response(error_message: str):
    """Return a standardized bad request response."""
    return custom_response(status_code=BAD_REQUEST_400, error=error_message)

def internal_server_error_response(error_message: str):
    """Return a standardized internal server error response."""
    return custom_response(status_code=INTERNAL_SERVER_ERROR_500, error=error_message)

def success_response(data: dict or list):
    """Return a standardized success response."""
    return custom_response(status_code=OK_200, data=data)
