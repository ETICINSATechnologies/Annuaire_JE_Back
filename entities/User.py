#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, String

from util.db_config import Base
from util.encryption import encrypt, create_password, create_temp_password


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    tempPassword = Comumn(String, nullable=False)

    def __init__(self, username):
        self.username = username
        self.password = create_password()
        self.tempPassword = self.password

    def update(self, password=None):
        if password:
            self.password = encrypt(password)

    def update_temp_pass(self):
        self.tempPassword = create_temp_password()

    def serialize(self):
        return {
            'username': self.username,
            'password': self.password
        }

