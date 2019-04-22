#!/usr/bin/env python3
# coding: utf8

import os
import re

from flask import safe_join

from util.log import info_logger

UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx'}


def get_extension(filename):
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()


def save(file, member_id=None):
    try:
        extension = get_extension(file.filename)
        if extension in ALLOWED_EXTENSIONS:
            location = "data.xlsx"
            if member_id:
                old_file = find_image(member_id)
                if old_file:
                    delete_image(old_file)
                location = f'{member_id}.{extension}'
            file.save(os.path.join(UPLOAD_FOLDER, location))
            return location
    except Exception as e:
        info_logger.error(e)


def delete_image(file):
    os.remove(os.path.join(UPLOAD_FOLDER, file))


def find_image(member_id):
    pattern = f'^{member_id}\.[a-z]+$'
    rex = re.compile(pattern)
    files = os.listdir(
        safe_join(os.getcwd(), UPLOAD_FOLDER))
    for file in files:
        if rex.search(file):
            return file
