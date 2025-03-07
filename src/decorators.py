from functools import wraps
import logging
from time import time


def log(filename=None):
    """
        Данный декоратор обертывает функцию и логирует её выполнение. В случае успешного выполнения функции,
        в логи записывается сообщение "status ok". Если возникает исключение, то в логи записывается информация
        об имени функции, классе исключения, аргументах и ключевых словах, а также сообщение "not ok".
        """

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
