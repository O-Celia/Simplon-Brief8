#!/usr/bin/env python3
# coding: utf-8
# vi: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import sys
import requests
import threading
import random
import time
import requests_toolbelt
import concurrent.futures as cf
from datetime import datetime as dt
from requests_toolbelt.multipart.encoder import MultipartEncoder as Form

URL = "http://20.199.58.218:80/"


def make_form(value):
    f = Form({'vote': 'value'})
    return f.content_type, f.to_string()


f_cats_ct, f_cats = make_form('Maël')
f_dogs_ct, f_dogs = make_form('Florian')
f_reset_ct, f_reset = make_form('Reset')

quit = threading.Event()


def send_votes(thread_id: int, quit: threading.Event):
    j = 0
    while not quit.is_set():
        f, ct = random.choice(((f_cats, f_cats_ct), (f_dogs, f_dogs_ct)))
        r = requests.post(URL, data=f, headers={'Content-Type': ct})
        j += 1
        if not r.ok:
            print(f"[{dt.now()}] thread {thread_id}, request {j}: Error {r.status_code}")
            continue

        print(f"[{dt.now()}] thread {thread_id}, request {j}: {r.headers['X-HANDLED-BY']}")


def main():
    print(f"[{dt.now()}] Début du test")

    quits = []
    with cf.ThreadPoolExecutor(10) as exc:
        try:
            for i in range(1, 10, 2):
                q = threading.Event()
                quits.append(q)
                exc.submit(send_votes, i, q)
                exc.submit(send_votes, i + 1, q)
                time.sleep(300)

            for q in quits:
                q.set()
                time.sleep(300)
        except KeyboardInterrupt:
            pass

        for q in quits:
            q.set()

    print(f"[{dt.now()}] Fin du test")
    return


if __name__ == '__main__':
    sys.exit(main())
