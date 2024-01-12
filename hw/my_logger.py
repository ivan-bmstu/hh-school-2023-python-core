from time import perf_counter
from datetime import datetime


class MyLogger:

    @staticmethod
    def log_func_start_time_duration(target_func):

        def inner_func(*args, **kwargs):
            start = perf_counter()
            print("//////////////////////////////////////")
            print(f"Init for function {target_func.__qualname__} at {datetime.now()}")
            result = target_func(*args, **kwargs)
            end = perf_counter()
            print(f"Function {target_func.__qualname__} finish at {datetime.now()}")
            print(f"The execution time of the function {target_func.__qualname__} was {(end - start)}s")
            print(r"\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
            return result

        return inner_func
