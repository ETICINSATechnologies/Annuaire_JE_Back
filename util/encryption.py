#!/usr/bin/env python3
# coding: utf8

import json
import hmac
import base64
import hashlib
import random
import string
import time
import decimal

from passlib.hash import pbkdf2_sha256

from util.Exception import AuthError
from util.VarConfig import VarConfig
from util.log import info_logger


def create_password():
    return ''.join(random.SystemRandom().choice(
            string.ascii_letters + string.digits) for i in range(15))

def create_temp_password():
    temp=  ''.join(random.SystemRandom().choice(
            string.ascii_letters + string.digits) for i in range(15))
    info_logger.error(temp)
    return temp


def encrypt(password):
    return pbkdf2_sha256.encrypt(password)


def is_password_valid(hash_password, hash_temp_password, temp_refresh_time, password):
    #return pbkdf2_sha256.verify(password, hash_password)
    info_logger.error(hash_temp_password)
    valid = pbkdf2_sha256.verify(password, hash_password)
    if not valid : 
        valid = (decimal.Decimal(time.time())-temp_refresh_time < 7200) and pbkdf2_sha256.verify(password, hash_temp_password)

    return valid


def jwt_encode(payload):
    header = json.dumps({
        'alg': 'HS256',
        'typ': 'JWT'
    })

    encoded_header = encode_base64(header)
    encoded_payload = encode_base64(json.dumps(payload))

    secret_key = bytes(VarConfig.get()['password'], 'utf-8')
    message = f'{encoded_header}.{encoded_payload}'

    signature = hmac.new(
        secret_key, message.encode('utf-8'), hashlib.sha256).hexdigest()
    encoded_signature = encode_base64(signature)

    return f'{message}.{encoded_signature}'


def jwt_decode(jwt):
    try:
        encoded_header, encoded_payload, encoded_signature \
            = jwt.split('.')

        secret_key = bytes(VarConfig.get()['password'], 'utf-8')
        message = f'{encoded_header}.{encoded_payload}'

        signature = hmac.new(
            secret_key, message.encode('utf-8'),
            hashlib.sha256).hexdigest()

        if encoded_signature == encode_base64(signature):
            return json.loads(decode_base64(encoded_payload))
    except Exception:
        raise AuthError


def encode_base64(string):
    string = base64.b64encode(bytes(string, 'utf-8')).decode('utf-8')
    return string.translate(str.maketrans({
        '+': '-', '/': '_', '=': ''
    }))


def decode_base64(string):
    string += len(string) % 4 * '='
    return base64.b64decode(string).decode('utf-8')


if __name__ == '__main__':
    print(jwt_decode(jwt_encode({
        'id': 1,
        'username': 'cool'
    })))
