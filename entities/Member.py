#!/usr/bin/env python3
# coding: utf8
import unicodedata

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from entities.MemberPosition import MemberPosition
from entities.User import User
from util.db_config import Base
from util.serialize import serialize


class Member(Base):
    __tablename__ = "member"

    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    birthday = Column(String)
    gradeYear = Column(Integer)
    telephone = Column(String)
    gender = Column(String)
    facebook = Column(String)
    linkedin = Column(String)
    company = Column(String)

    user = relationship("User",
                        uselist=False,  # one instance only
                        cascade="all, delete-orphan",
                        single_parent=True)

    positions = relationship('MemberPosition',
                             cascade="all, delete-orphan")

    def __init__(self):
        pass

    def __str__(self):
        return str(self.serialize())

    def update(self, new_values):
        for att_key, att_val in new_values.items():
            if hasattr(self, att_key):
                if not att_val:
                    att_val = None
                elif isinstance(att_val, str):
                    att_val = att_val.lower()
                setattr(self, att_key, att_val)

        if self.user and 'password' in new_values:
            self.user.update(new_values['password'])

        return self

    def create_user(self):
        username = f'{self.firstName.lower()}.{self.lastName.lower()}'
        username = unicodedata.normalize('NFD', username) \
            .encode('ascii', 'ignore')

        self.user = User(username.decode('utf-8').replace(' ', '-'))

    def set_positions(self, positions):
        self.positions = []
        if positions:
            for position in positions:
                if 'id' in position and position['id'] \
                        and 'year' in position and position['year']:
                    member_position = MemberPosition(
                        position['id'], position['year']
                    )
                    self.positions.append(member_position)

    @classmethod
    def get_attr(cls, attr_name):
        if hasattr(cls, attr_name):
            return getattr(cls, attr_name)
        return None

    def get_all_attr(self):
        return {
            i for i in dir(self)
            if not (i.startswith('_')
                    or callable(getattr(self, i))
                    or i == "metadata" or i == 'user')
        }

    def serialize(self):
        serialized_object = {
            'username': self.user.username
        }

        for attr in self.get_all_attr():
            serialized_object[attr] = serialize(getattr(self, attr))
        return serialized_object
