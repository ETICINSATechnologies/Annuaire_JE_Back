#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, String, Numeric
from time import time
from util.db_config import Base
from util.encryption import encrypt, create_password, create_temp_password


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    temp_password = Column(String)
    temp_refresh_time = Column(Numeric)

    def __init__(self, username):
        self.username = username

    def update(self, password=None):
        if password:
            self.password = encrypt(password)


    def update_temp_pass(self):
        temp_pass = create_temp_password()
        self.temp_password = encrypt(temp_pass)
        self.temp_refresh_time=time()
        return temp_pass

    def serialize(self):
        return {
            'username': self.username,
            'password': self.password
        }

