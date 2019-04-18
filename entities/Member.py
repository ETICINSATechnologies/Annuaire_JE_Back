#!/usr/bin/env python3
# coding: utf8
import unicodedata

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from entities.User import User
from util.db_config import Base
from util.serialize import serialize
from util.encryption import encrypt


class Member(Base):
    __tablename__ = "member"

    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    birthday = Column(String)
    gradeYear = Column(Integer)
    telephone = Column(String)

    user = relationship("User",
                        uselist=False,  # one instance only
                        cascade="all, delete-orphan",
                        single_parent=True)

    def __init__(self):
        pass

    def __str__(self):
        return str(self.serialize())

    def update(self, new_values):
        for att_key, att_val in new_values.items():
            if hasattr(self, att_key):
                setattr(self, att_key, att_val)

        username = f'{self.firstName.lower()}.{self.lastName.lower()}'
        username = unicodedata.normalize('NFD', username) \
            .encode('ascii', 'ignore')

        self.user = User(username.decode('utf-8'))

        if 'password' in new_values:
            self.user.update(new_values['password'])

        return self

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
                    or i == "metadata")
        }

    def serialize(self):
        serialized_object = {}
        for attr in self.get_all_attr():
            serialized_object[attr] = serialize(getattr(self, attr))
        return serialized_object


if __name__ == "__main__":
    m = Member()
    m.update({
        'firstName': 'Louis'
    })
    print(m)
