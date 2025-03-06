from functools import wraps
import logging
from time import time


def log(filename=None):

    def decorator(func):

        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
                if filename:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(f"{func.__name__} status ok\n")
                else:
                    print(f"{func.__name__} status ok")
            except Exception as e:
                if filename:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(f"{func.__name__}, {e.__class__.__name__}, {args}, {kwargs} not ok\n")
                else:
                    print(f"{func.__name__}, {e.__class__.__name__}, {args}, {kwargs} not ok")

            return func(*args, **kwargs)

        return wrapper

    return decorator
