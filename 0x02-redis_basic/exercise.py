#!/usr/bin/env python3
"""
this module implement redis basic function
"""
from typing import Union, Callable, Optional
import redis
import uuid
import functools


def count_calls(method: Callable) -> Callable:
    """
    this decorator count the times methos were called
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        the wrapper methos thats increment the call count
        then call the origina; method
        """

        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    thos decorator store history of input and output for a fuction
    """
    @functool.wraps(methos)
    def wrapper(self, *args, **kwargs):
        """
        the wrapper methos thaats logs the input and output
        """

        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)

        self._redis.rpush(output_key, output)
        return output

    return wrapper


class Cache:
    """ the class cache """
    def __init__(self):
        """
        The init method
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        this method generate a random key
        store the random key using redis
        then return the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, float, int, bytes, None]:
        """
        Get method implementing geting cammand
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """
        This method implment get
        and return an optinal str
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: int) -> Optional[int]:
        """
        this methis implement get
        then return optional int
        """
        return self.get(key, fn=int)
