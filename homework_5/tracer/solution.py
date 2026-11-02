from contextvars import ContextVar
from functools import wraps


_depth = ContextVar("tracer_depth", default=0)


def tracer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        depth = _depth.get()
        indent = "  " * depth
        arguments = [repr(arg) for arg in args]
        arguments.extend(f"{key}={value!r}" for key, value in kwargs.items())
        print(f"{indent}-> {func.__name__}({', '.join(arguments)})")
        token = _depth.set(depth + 1)
        try:
            result = func(*args, **kwargs)
        except Exception as error:
            print(f"{indent}!! {func.__name__}: {error!r}")
            raise
        else:
            print(f"{indent}<- {func.__name__} = {result!r}")
            return result
        finally:
            _depth.reset(token)

    return wrapper


if __name__ == "__main__":
    @tracer
    def factorial(n):
        if n <= 1:
            return 1
        return n * factorial(n - 1)

    factorial(3)
