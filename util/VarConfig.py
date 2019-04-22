#!/usr/bin/env python3
# coding: utf8

import os


class VarConfig:
    @staticmethod
    def get():
        config = {}
        with open(".env", 'r') as file:
            for line in file.readlines():
                var, value = line.replace('\n', '').split('=')
                config[var] = value

            # if the environment variable "EXTENDED_DOC_PASSWORD" exists
            if os.environ.get("EXTENDED_DOC_PASSWORD"):
                config['password'] = os.environ["EXTENDED_DOC_PASSWORD"]

            return config


if __name__ == '__main__':
    print(VarConfig.get())
