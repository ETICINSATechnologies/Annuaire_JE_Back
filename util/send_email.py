#!/usr/bin/env python3
# coding: utf8

from __future__ import print_function

import base64
import pickle
import os.path
import time
from email.mime.text import MIMEText
from enum import Enum

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from util.VarConfig import VarConfig

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

sender_email = VarConfig.get()['email']
je_name = VarConfig.get()['je_name']
yearbook_url = VarConfig.get()['yearbook_url']

with open('email_template', 'r', encoding='utf-8') as file:
    template_email = file.read()

with open('reset_email_template', 'r', encoding='utf-8') as file:
    reset_template_email = file.read()


class EmailError(Exception):
    pass


class EmailStatus(Enum):
    not_defined = 0
    no_json_credentials = 1
    no_access_token = 2
    access_token = 3


class Email:
    creds = None
    flow = None
    status = 'not_defined'
    service = None

    @classmethod
    def send_registration_email(cls, member, password):
        firstName = member.firstName
        lastName = member.lastName
        email = member.email
        username = member.user.username

        message_text = eval(f'f"""{template_email}"""')

        message = cls.create_email(
            sender_email, email,
            f'{je_name} - Inscription annuaire des anciens',
            message_text)

        if not cls.service:
            Email.set_status()
            if not cls.service:
                raise EmailError

        cls.service.users().messages().send(
            userId='me', body=message).execute()

    @classmethod
    def send_reset_email(cls, member, temp_password):
        firstName = member.firstName
        lastName = member.lastName
        email = member.email
        username = member.user.username

        message_text = eval(f'f"""{reset_template_email}"""')

        message = cls.create_email(
            sender_email, email,
            f'{je_name} - Annuaire des anciens - Reset mot de passe',
            message_text)

        if not cls.service:
            Email.set_status()
            if not cls.service:
                raise EmailError

        cls.service.users().messages().send(
            userId='me', body=message).execute()

    @staticmethod
    def create_email(sender, to, subject, message_text):
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return \
            {'raw': base64.urlsafe_b64encode(
                message.as_bytes()).decode()}

    @classmethod
    def set_status(cls):
        response = {}

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                cls.creds = pickle.load(token)
                cls.status = 'access_token'
                cls.service = build(
                    'gmail', 'v1', credentials=cls.creds
                )

        if not os.path.exists('credentials.json'):
            cls.status = 'no_json_credentials'

        elif not cls.creds or not cls.creds.valid:
            if cls.creds and cls.creds.expired \
                    and cls.creds.refresh_token:
                cls.creds.refresh(Request())
            else:
                cls.flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES,
                    redirect_uri='urn:ietf:wg:oauth:2.0:oob')
                cls.status = 'no_access_token'
                response['url'] = cls.flow.authorization_url()[0]

        response['status'] = cls.status

        return response

    @classmethod
    def create_token(cls, token_code):
        if cls.flow:
            cls.flow.fetch_token(code=token_code)
            cls.creds = cls.flow.credentials
            cls.status = EmailStatus.access_token

            with open('token.pickle', 'wb') as token:
                pickle.dump(Email.creds, token)
                cls.flow = None


Email.set_status()
