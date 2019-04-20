#!/usr/bin/env python3
# coding: utf8

from util.VarConfig import VarConfig
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
default_db_info = ('postgresql://'
                   'postgres:password@localhost:5433/extendedDoc')


def get_db_info():
    config = VarConfig.get()

    return f'{config["ordbms"]}://{config["user"]}:' \
           f'{config["password"]}@{config["host"]}:' \
           f'{config["port"]}/{config["dbname"]}'
