#!/usr/bin/env python3
# coding: utf8

import os
import yaml


class VarConfig:
    @staticmethod
    def get():
        with open("util/config.yml", 'r') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

            # if the environment variable "EXTENDED_DOC_PASSWORD" exists
            if os.environ.get("EXTENDED_DOC_PASSWORD"):
                config['password'] = os.environ["EXTENDED_DOC_PASSWORD"]

            return config