from rest_framework.exceptions import APIException

from .messages import CUSTOM_API_EXCEPTION


class CustomAPIException(APIException):
    status_code = 400
    default_detail = CUSTOM_API_EXCEPTION
