#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, String

from util.db_config import Base
from util.encryption import encrypt


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    def __init__(self, username):
        self.username = username

    def update(self, password):
        self.password = encrypt(password)
        return self

    def serialize(self):
        return {
            'username': self.username,
            'password': self.password
        }

