# -*- coding: utf-8 -*-

import re
import random
import string


def generate_password(digits=6):
    """."""
    password = ''.join(random.choice(
        string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(digits))
    return password


def prepare_string(s):
    """."""
    return s.encode('utf-8').strip()


def valid_email(email):
    """."""
    pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
    if email:
        if re.match(pattern, email):
            return True
    return False
