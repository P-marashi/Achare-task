"""
All the project regexes will be declare in here.
These regexes can be used in somewhere of our project
eg: models, forms, serializers
"""

import re


def phone_number_regex(phone_number):
    # Pattern: starts with 09 followed by 9 digits
    return re.match(r"^09\d{9}$", phone_number)