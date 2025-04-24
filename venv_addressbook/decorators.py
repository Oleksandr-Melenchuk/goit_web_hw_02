def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, KeyError, IndexError, AttributeError) as error:
            return f"Error {error}"

    return inner
