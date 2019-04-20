#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from util.db_config import Base


class MemberPosition(Base):
    __tablename__ = "member_position"

    id = Column(Integer, primary_key=True)

    member_id = Column(Integer,
                       ForeignKey("member.id"))

    position_id = Column(Integer,
                         ForeignKey("position.id",
                                    ondelete="CASCADE"))

    pos = relationship("Position")
    year = Column(Integer)

    def __init__(self, position_id, year):
        self.position_id = position_id
        self.year = year

    def __str__(self):
        return f'm_id: {self.member_id} p_id:{self.position_id}, ' \
               f'year:{self.year}'

    @classmethod
    def get_attr(cls, attr_name):
        if hasattr(cls, attr_name):
            return getattr(cls, attr_name)
        return None

    def get_all_attr(self):
        return {i for i in dir(self)
                if not (i.startswith('_')
                        or callable(getattr(self, i))
                        or i == "metadata")}

    def serialize(self):
        return {
            'label': self.pos.label,
            'year': self.year
        }
