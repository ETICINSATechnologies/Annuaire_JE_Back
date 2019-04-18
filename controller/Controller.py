#!/usr/bin/env python3
# coding: utf8

from util.db_config import *
import persistence_unit.PersistenceUnit as pUnit

from entities.User import User
from entities.Member import Member


class Controller:
    """
    Class that allows communication with the DB
    No instance is needed because all its methods are static.
    This methods are used to make a CRUD operation,
    by making a query or a transaction with the DB by using
    the decorators '~persistence_unit.PersistenceUnit.make_a_query'
    and make_a_transaction
    """

    @staticmethod
    def recreate_tables():
        Base.metadata.drop_all(pUnit.engine)
        Base.metadata.create_all(pUnit.engine)
        Controller.create_user()

    @staticmethod
    def create_tables():
        Base.metadata.create_all(pUnit.engine)
        Controller.create_user()

    @staticmethod
    @pUnit.make_a_transaction
    def create_user(session):
        password = 'password'
        user = User('admin')
        user.update("password")
        session.add(user)


if __name__ == '__main__':
    Controller.recreate_tables()
