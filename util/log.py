#!/usr/bin/env python3
# coding: utf8

import logging
import os

print(os.getcwd())

default_formatter = '[%(levelname)s] %(asctime)s : %(message)s'


def set_logger(a_logger, level, file_name, mode, formatter):
    a_logger.setLevel(level)
    file_handler = logging.FileHandler(file_name, mode=mode)
    formatter = logging.Formatter(formatter)
    file_handler.setFormatter(formatter)
    a_logger.addHandler(file_handler)


info_logger = logging.getLogger('sqlalchemy.engine')
set_logger(info_logger, logging.DEBUG, 'log/sqlalchemy.log', 'w',
           default_formatter)

info_logger = logging.getLogger('sqlalchemy.engine')
set_logger(info_logger, logging.INFO, 'log/sqlalchemy_info.log', 'w',
           default_formatter)

info_logger = logging.getLogger('info_logger')
set_logger(info_logger, logging.DEBUG, 'log/info.log', 'w',
           default_formatter)
