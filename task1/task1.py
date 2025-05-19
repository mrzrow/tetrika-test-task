import inspect
from functools import wraps

def strict(func):
    sig = inspect.signature(func)
    annotations = func.__annotations__

    @wraps(func)
    def inner(*args, **kwargs):
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        for name, value in bound_args.arguments.items():
            if name in annotations:
                expected_type = annotations[name]
                if not isinstance(value, expected_type):
                    raise TypeError(f"Argument '{name}' expected {expected_type.__name__}, got {type(value).__name__}")

        result = func(*args, **kwargs)

        if 'return' in annotations:
            expected_return = annotations['return']
            if not isinstance(result, expected_return):
                raise TypeError(f"Return value expected {expected_return.__name__}, got {type(result).__name__}")
        
        return result

    return inner


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


print(sum_two(1, 2))  # >>> 3
print(sum_two(1, 2.4))  # >>> TypeError