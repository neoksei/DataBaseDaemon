import threading
import json
import lockfile
from vk_model import Link, Image, Text


class ImageThread(threading.Thread):
    def __init__(self, fname, thread_mutex, event, barrier):
        super().__init__()
        self.fname = fname
        self.thread_mutex = thread_mutex
        self.event = event
        self.barrier = barrier
        self.i = 0
        self.ipc_lock = lockfile.FileLock(fname)

    def run(self):
        while True:
            self.event.wait()
            self.ipc_lock.acquire()
            with open(self.fname, 'r') as f:
                items = json.load(f)
            self.ipc_lock.release()

            for item in items:
                query = Image.select().where(Image.feed_id == item['feed_id'])
                if query.exists():
                    continue
                self.thread_mutex.acquire()
                row = Image(**item)
                row.save()
                self.thread_mutex.release()
            self.barrier.wait()


class LinkThread(threading.Thread):
    def __init__(self, fname, thread_mutex, event, barrier):
        super().__init__()
        self.fname = fname
        self.thread_mutex = thread_mutex
        self.event = event
        self.barrier = barrier
        self.ipc_lock = lockfile.FileLock(fname)

    def run(self):
        while True:
            self.event.wait()
            self.ipc_lock.acquire()
            with open(self.fname, 'r') as f:
                items = json.load(f)
            self.ipc_lock.release()

            for item in items:
                query = Link.select().where(Link.feed_id == item['feed_id'])
                if query.exists():
                    continue
                self.thread_mutex.acquire()
                row = Link(**item)
                row.save()
                self.thread_mutex.release()
            self.barrier.wait()


class TextThread(threading.Thread):
    def __init__(self, fname, thread_mutex, event, barrier):
        super().__init__()
        self.fname = fname
        self.thread_mutex = thread_mutex
        self.event = event
        self.barrier = barrier
        self.ipc_lock = lockfile.FileLock(fname)

    def run(self):
        while True:
            self.event.wait()
            self.ipc_lock.acquire()
            with open(self.fname, 'r') as f:
                items = json.load(f)
            self.ipc_lock.release()

            for item in items:
                query = Text.select().where(Text.feed_id == item['feed_id'])
                if query.exists():
                    continue
                self.thread_mutex.acquire()
                row = Text(**item)
                row.save()
                self.thread_mutex.release()
            self.barrier.wait()
