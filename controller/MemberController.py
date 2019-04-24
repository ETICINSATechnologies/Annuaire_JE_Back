#!/usr/bin/env python3
# coding: utf8

from math import ceil
from time import time

import sqlalchemy.orm

from entities.User import User
from entities.Member import Member
from entities.MemberPosition import MemberPosition
from entities.Position import Position
# from util.send_email import Email
from util.Exception import LoginError
from util.encryption import jwt_encode, create_password
from util.encryption import is_password_valid
import persistence_unit.PersistenceUnit as pUnit
from util.serialize import serialize


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
        try:
            username = args[0]['username']
            password = args[0]['password']

            user = session.query(User).filter(
                User.username == username).one()

            if is_password_valid(user.password, password):
                exp = time() + 24 * 3600
                payload = {
                    'id': user.id,
                    'username': user.username,
                    'exp': exp
                }
                return {
                    "token": jwt_encode(payload)
                }
        except sqlalchemy.orm.exc.NoResultFound:
            pass

        raise LoginError

    @staticmethod
    @pUnit.make_a_transaction
    def create_member(session, *args):
        attributes = args[0]
        member = Member()
        positions = attributes.pop('positions', None)
        password = create_password()
        member.set_positions(positions)
        member.update(attributes)
        member.create_user(password)
        session.add(member)
        session.flush()  # flush the member without committing
        # Email.send_registration_email(member, password)
        return member

    @staticmethod
    @pUnit.make_a_query
    def get_member_by_id(session, *args):
        member_id = args[0]
        return session.query(Member).filter(
            Member.id == member_id).one()

    @staticmethod
    @pUnit.make_a_query
    def get_members(session, *args):
        attributes = {}
        page_number = 0
        page_size = 25

        if len(args) > 0:
            attributes = {
                key: args[0].get(key).lower()
                if isinstance(args[0].get(key), str)
                else args[0].get(key)
                for key in args[0].keys()
            }

        if 'pageNumber' in attributes:
            page_number = int(attributes.pop('pageNumber'))

        if 'pageSize' in attributes:
            page_size = int(attributes.pop('pageSize'))

        if 'positionId' in attributes:
            attributes['position_id'] = attributes.pop('positionId')

        positions_params = {
            key: attributes.pop(key)
            for key in
            {'position_id', 'year'}.intersection(set(attributes.keys()))
        }

        members = session.query(Member).filter_by(**attributes)

        if positions_params:
            members.join(MemberPosition).filter_by(**positions_params)

        page = members.limit(page_size).offset(page_number * page_size)

        total_items = members.group_by(Member).count()
        total_page = ceil(total_items / page_size)

        return {
            'content': serialize(page.all()),
            'meta': {
                'page': page_number,
                'totalPages': total_page,
                'totalItems': total_items,
                'itemsPerPage': page_size
            }
        }

    @staticmethod
    @pUnit.make_a_transaction
    def update_member(session, *args):
        member_id = args[0]
        attributes = args[1]

        member = session.query(Member) \
            .filter(Member.id == member_id).one()

        positions = attributes.pop('positions', None)
        member.set_positions(positions)
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

    @staticmethod
    @pUnit.make_a_query
    def get_positions(session, *args):
        return session.query(Position).all()
