# -*- coding: utf-8 -*-
import os
from hashlib import sha256

SALT_ENV_VAR = 'CSCI_SALT'

def get_csci_salt():

    """Returns the appropriate salt for CSCI E-29
    :rtype: bytes

    """

    # Hint: use os.environment and bytes.fromhex
    raw_salt = os.getenv(SALT_ENV_VAR, default='')

    if not raw_salt:
        raise ValueError("Empty salt!")

    return bytes.fromhex(raw_salt)


def _as_bytes(val):
    if isinstance(val, str):
        return val.encode()
    return val

def hash_str(some_val, salt=''):

    """Converts strings to hash digest
    See: https://en.wikipedia.org/wiki/Salt_(cryptography)
    :param str or bytes some_val: thing to hash
    :param str or bytes salt: string or bytes to add randomness to the hashing,
       defaults to ''.
    :rtype: bytes

    """
    return sha256(
        _as_bytes(salt) + _as_bytes(some_val)
    ).digest()


def get_user_id(username):
    salt = get_csci_salt()
    return hash_str(username.lower(), salt=salt).hex()[:8]
