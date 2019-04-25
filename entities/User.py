#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, String

from util.db_config import Base
from util.encryption import encrypt, create_password


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    def __init__(self, username):
        self.username = username
        self.password = create_password()

    def update(self, password=None):
        if password:
            self.password = encrypt(password)

    def serialize(self):
        return {
            'username': self.username,
            'password': self.password
        }

