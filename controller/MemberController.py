#!/usr/bin/env python3
# coding: utf8

from time import time
import persistence_unit.PersistenceUnit as pUnit

from entities.User import User
from entities.Member import Member
from util.Exception import LoginException
from util.encryption import jwt_encode
from util.encryption import is_password_valid


class MemberController:
    """
    Class that allows communication with the DB
    No instance is needed because all its methods are static.
    This methods are used to make a CRUD operation,
    by making a query or a transaction with the DB by using
    the decorators '~persistence_unit.PersistenceUnit.make_a_query'
    and make_a_transaction
    """

    @staticmethod
    @pUnit.make_a_transaction
    def login(session, *args):
        username = args[0]['username']
        password = args[0]['password']

        user = session.query(User).filter(
            User.username == username).one()

        if user and is_password_valid(user.password, password):
            exp = time() + 24 * 3600
            payload = {
                'id': user.id,
                'username': user.username,
                'exp': exp
            }
            return jwt_encode(payload)

        raise LoginException

    @staticmethod
    @pUnit.make_a_transaction
    def create_member(session, *args):
        attributes = args[0]
        member = Member()
        member.update(attributes)
        session.add(member)
        return member

    @staticmethod
    @pUnit.make_a_query
    def get_member_by_id(session, *args):
        member_id = args[0]
        return session.query(Member).filter(
            Member.id == member_id).one()

    @staticmethod
    @pUnit.make_a_transaction
    def get_members(session, *args):
        attributes = {}
        if len(args) > 0:
            attributes = {key: args[0].get(key)
                          for key in args[0].keys()
                          if key != "password"}
        return session.query(Member).filter_by(**attributes)

    @staticmethod
    @pUnit.make_a_transaction
    def update_member(session, *args):
        member_id = args[0]
        attributes = args[1]

        member = session.query(Member) \
            .filter(Member.id == member_id).one()
        member.update(attributes)
        session.add(member)

        return member

    @staticmethod
    @pUnit.make_a_transaction
    def delete_member(session, *args):
        member_id = args[0]
        member = session.query(Member).filter(
            Member.id == member_id).one()
        session.delete(member)