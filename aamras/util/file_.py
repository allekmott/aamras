"""File utility functions."""

from contextlib import contextmanager
import os
import os.path

@contextmanager
def deleting(file_path: str):
    """Context manager; Silently deletes a specified file on __exit__.

    :param file_path: path of file to be deleted
    """
    try:
        yield
    finally:
        if os.path.exists(file_path):
            os.unlink(file_path)
