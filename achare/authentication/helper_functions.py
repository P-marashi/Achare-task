import logging
import random
import uuid
from typing import Any

from .auth_blocking import redis_cache

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_client_ip(request: Any) -> str:
    """
    Retrieve the client IP address from the request.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def send_otp(otp: int, mobile_number: str) -> bool:
    """
    Send an OTP to the given mobile number.
    """
    # thi is sample for sending sms
    # def send_sms_password(code: int, phone: str):
    # url = env('SEND_LOOKUP_ENDPOINT')
    # data = {
    #     'sms_id': uuid.uuid4().hex,
    #     'receptor': [phone],
    #     'message': code,
    #     'template_name': env('LOOKUP_TEMPLATE_NAME'),
    #     'message_type': 'sms',
    # }
    # response = requests.post(url=url, json=data)
    # if response.status_code != 200:
    #     raise ApplicationError(_('SMS system is unavailable'))
    return True


def generate_send_and_cache_otp(mobile_number: str) -> str:
    """
    Generate, send, and cache an OTP for the given mobile number.
    Returns the generated OTP.
    """
    otp = random.randint(100000, 999999)
    redis_cache.set(f"otp:{mobile_number}", str(otp), ex=300)
    redis_cache.get(f"otp:{mobile_number}")
    send_otp(otp, mobile_number)
    logger.debug(f"Generated and sent OTP: {otp}")
    return str(otp)


def generate_and_cache_nonce(mobile_number: str) -> str:
    """
    Generate and cache a nonce for the given mobile number.
    Returns the generated nonce.
    """
    nonce = str(uuid.uuid4())
    redis_cache.set(f"hash:{nonce}", str(mobile_number), ex=300)
    logger.debug(f"Generated and cached nonce: {nonce}")
    return nonce
