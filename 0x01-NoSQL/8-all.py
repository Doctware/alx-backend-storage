#!/usr/bin/env python3
""" this module ccontains a prototype that list the DOC
    in the provided collection """


def list_all(mongo_collection):
    """
    this fuction returns the list of Dcoument in collection
    But return empty list if DOC not fund in collection
    """
    return list(mongo_collection.find())
