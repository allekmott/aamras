
from contextlib import contextmanager
import os
import os.path

@contextmanager
def deleting(file_name: str):
    try:
        yield
    finally:
        if os.path.exists(file_name):
            os.unlink(file_name)
