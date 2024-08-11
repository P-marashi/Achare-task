import uuid
import random


def otp_code():
    """
    All the project random numbers will be declare in here.
    These randoms can be used in anywhere of our project
    """
    return random.randrange(100000, 999999)


def send_otp(test1, test2):
    """
    ..
    """
    return True


def generate_unique_hash():
    """
    this func will use to generate unique hash,
    and it use for authentication user
    """
    return str(uuid.uuid4())


