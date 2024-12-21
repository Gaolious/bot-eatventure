from functools import wraps


class ResetRepeatCountException(Exception):
    pass

class ExitRepeatException(Exception):
    pass

def repeat_retry(repeat):
    def decorator(func):
        @wraps(func)
        def fn(*args, **kwargs):
            attempt = 0
            while attempt < repeat:
                try:
                    func(*args, **kwargs)
                    attempt += 1
                except ResetRepeatCountException:
                    attempt = 0
                except ExitRepeatException:
                    return True
            return False
        return fn
    return decorator


