#!/usr/bin/env python3
""" this module contains a prototype thats insert Document into a
    provided collection """


def insert_school(mongo_collection, **kwargs):
    """
    this function insert a documet into a colection
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
