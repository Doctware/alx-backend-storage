#!/usr/bin/env python3
"""
this module implement expiring web cache tracher
"""
import requests
import redis
import time
from typing import Callable

# Initialize Redis client
redis_client = redis.Redis()

def cache_url(method: Callable) -> Callable:
    """Decorator to cache the URL response and track access counts."""
    def wrapper(url: str) -> str:
        # Construct cache and count keys
        cache_key = f"cache:{url}"
        count_key = f"count:{url}"
        
        # Check if the response is cached
        cached_response = redis_client.get(cache_key)
        if cached_response:
            redis_client.incr(count_key)  # Increment access count
            return cached_response.decode('utf-8')
        
        # Make the request if not cached
        response = method(url)

        # Cache the response with an expiration time of 10 seconds
        redis_client.setex(cache_key, 10, response)
        redis_client.incr(count_key)  # Increment access count

        return response
    return wrapper

@cache_url
def get_page(url: str) -> str:
    """Fetch the HTML content of a particular URL."""
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    return response.text
