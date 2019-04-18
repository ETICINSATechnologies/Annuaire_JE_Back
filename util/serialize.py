#!/usr/bin/env python3
# coding: utf8


def serialize(objects_to_serialize):
    try:
        return objects_to_serialize.serialize()

    except AttributeError:
        try:
            doc_lists = []
            for obj in objects_to_serialize:
                doc_lists.append(obj.serialize())
            return doc_lists

        except (TypeError, AttributeError):
            return objects_to_serialize
