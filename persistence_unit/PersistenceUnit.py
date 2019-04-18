#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from util.db_config import get_db_info
from util.log import info_logger
from util.serialize import serialize

db_string = get_db_info("util/config.yml")
engine = create_engine(db_string)
Session = sessionmaker(engine)

"""
makeATransaction is a function that allows to re-use the same code
The function is split into two parts : 
everything below the keyword 'yield' and everything below
The first part of the code is first executed and return the variable 
after 'yield' (in this case 'session').
The one that calls the contextmanager executes then its code and can 
have access to the return variable
Finally the second part of the contextmanager is executed in all cases   
"""


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
