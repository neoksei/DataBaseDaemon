import signal
import os
import sys
import lockfile
import datetime
import fnames
from db_threads import *
from vk_model import db_handle, Image, Link, Text
import time

stop_request = False
pidfile = lockfile.FileLock('./db_seleniumd/db_seleniumd.pid')


def sigint_handler(signum, frame):
    print("[{}] Daemon stopped".format(str(datetime.datetime.now())))
    global stop_request
    stop_request = True


def sigcont_handler(signum, frame):
    print("[{}] Daemon started".format(str(datetime.datetime.now())))
    global stop_request
    stop_request = False


def sigterm_handler(signum, frame):
    print('[{}] Daemon receive signal SIGTERM'.format(str(datetime.datetime.now())))
    global pidfile
    pidfile.release()
    print('[{}] Daemon release lockfile'.format(str(datetime.datetime.now())))
    sys.stdout.close()
    sys.exit(-1)


def main():
    global pidfile
    try:
        pidfile.acquire(0)
    except lockfile.AlreadyLocked:
        sys.exit(-1)
    
    if not os.path.isdir('./db_seleniumd'):
        os.mkdir('./db_seleniumd')
        
    sys.stdout = open('./db_seleniumd/db_seleniumd.log', 'a')
    pid = os.getpid()
    with open('./db_seleniumd/db_seleniumd.pid', 'w') as f:
        f.write(str(pid))
    print("[{}] Daemon started".format(str(datetime.datetime.now())))
    thread_mutex = threading.Lock()
    event = threading.Event()
    barrier = threading.Barrier(4)
    threads = [(LinkThread(fnames.LINK, thread_mutex, event, barrier)),
               (ImageThread(fnames.IMAGE, thread_mutex, event, barrier)),
               (TextThread(fnames.TEXT, thread_mutex, event, barrier))]

    db_handle.connect()
    db_handle.create_tables([Text, Link, Image])

    for thread in threads:
        thread.daemon = True
        thread.start()

    signal.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGCONT, sigcont_handler)
    signal.signal(signal.SIGTERM, sigterm_handler)

    while True:
        event.set()
        event.clear()
        barrier.wait()
        barrier.reset()
        if stop_request:
            while not stop_request:
                time.sleep(1)
        else:
            time.sleep(3)


if __name__ == '__main__':
    fpid = os.fork()

    if fpid > 0:
        sys.exit(0)

    main()
    sys.exit(0)
