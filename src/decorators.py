def catch_errors(error_type, msg):
    def inner(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except error_type:
                return msg
        return wrapper
    return inner
        