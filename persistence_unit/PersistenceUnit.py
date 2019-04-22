#!/usr/bin/env python3
# coding: utf8

import sys
import time
from sqlalchemy.exc import OperationalError

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from util.log import info_logger
from util.db_config import get_db_info
from util.serialize import serialize


def try_to_connect():
    remaining_tries = 3
    while remaining_tries:
        try:
            print('Trying to connect to Database...')
            created_engine = create_engine(get_db_info())
            created_engine.connect()
            print('Connection succeed!')
            return created_engine
        except OperationalError:
            remaining_tries -= 1
            print('Connection failed', end=' ')
            if remaining_tries == 0:
                sys.exit()
            print('- new try')

            time.sleep(0.5)


def make_a_transaction(old_function):
    def new_function(*args):
        session = Session()
        response = None
        try:
            obj = old_function(session, *args)
            session.commit()
            response = serialize(obj)
        except Exception as e:
            info_logger.error(e)
            raise e
        finally:
            session.close()
        return response

    return new_function


def make_a_query(old_function):
    def new_function(attr):
        session = Session()
        response = None
        try:
            obj = old_function(session, attr)
            response = serialize(obj)
        except Exception as e:
            info_logger.error(e)
            raise e
        finally:
            session.close()
        return response

    return new_function


engine = try_to_connect()
Session = sessionmaker(engine)
