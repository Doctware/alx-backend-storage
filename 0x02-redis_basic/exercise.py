#!/usr/bin/env python3
"""
this module implement redis basic function
"""
from typing import Union
import redis
import uuid


class Cache:
    """ the class cache """
    def __init__(self):
        """
        The init method
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        this method generate a random key
        store the random key using redis
        then return the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
