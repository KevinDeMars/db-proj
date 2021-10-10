import contextlib
from typing import *
from threading import Semaphore

from db.file_manager import FileManager
from db.page import Page


class BufferManager:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = BufferManager()
        return cls._instance

    def __init__(self):
        self._buf: Dict[int, Tuple[Semaphore, Any]] = dict()

    def scan(self, pg_id):
        pass

    @contextlib.contextmanager
    def pin(self, pg_id):
        # TODO: Race condition if two threads create a semaphore for the same pg_id at same time
        if pg_id not in self._buf:
            self._buf[pg_id] = (Semaphore(1), FileManager.instance().read(pg_id))
            print(f"Loaded {pg_id}")

        semaphore, page = self._buf[pg_id]
        semaphore.acquire(blocking=True)
        yield page
        # implicitly wait until caller's "with" block is done
        semaphore.release()
