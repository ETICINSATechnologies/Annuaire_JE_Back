#!/usr/bin/env python3
# coding: utf8

import os
import yaml
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
default_db_info = ('postgresql://'
                   'postgres:password@localhost:5433/extendedDoc')


def get_db_info(config_file_name):
    with open(config_file_name, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

        # if the environment variable "EXTENDED_DOC_PASSWORD" exists
    if os.environ.get("EXTENDED_DOC_PASSWORD"):
        password = os.environ["EXTENDED_DOC_PASSWORD"]
        # otherwise we use the default password from 'config.yml'
    else:
        password = config["password"]

    db_info = \
        config['ordbms'] + "://" + \
        config["user"] + ":" + \
        password + "@" + \
        config["host"] + ":" + \
        str(config["port"]) + "/" + \
        config["dbname"]

    return db_info

# except (FileNotFoundError, KeyError):
#     return default_db_info
