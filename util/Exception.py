#!/usr/bin/env python3
# coding: utf8


class LoginError(Exception):
    pass


class FormatError(Exception):
    pass


class AuthError(Exception):
    pass


class SuccessNoBody(Exception):
    pass


class NotFound(Exception):
    pass
