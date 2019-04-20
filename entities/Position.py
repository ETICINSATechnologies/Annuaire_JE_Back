#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, String

from util.db_config import Base


class Position(Base):
    __tablename__ = "position"

    id = Column(Integer, primary_key=True)
    label = Column(String, nullable=False, unique=True)

    def __init__(self, label):
        self.label = label

    def serialize(self):
        return {
            'id': self.id,
            'label': self.label
        }
