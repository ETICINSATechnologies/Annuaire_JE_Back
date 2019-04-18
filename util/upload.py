#!/usr/bin/env python3
# coding: utf8

import os

from util.log import info_logger

UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = {'xls', 'xlsm', 'csv'}


def get_extension(filename):
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()


def allowed_file(extension):
    return extension in ALLOWED_EXTENSIONS


def save_file(filename, file):
    try:
        extension = get_extension(file.filename)
        if extension in ALLOWED_EXTENSIONS:
            location = str(filename) + '.' + extension
            file.save(os.path.join(UPLOAD_FOLDER, location))
            return location
    except Exception as e:
        info_logger.error(e)
        return None
