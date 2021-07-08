import random
import time
from threading import Thread

import requests

from client.proxy_choice import get_lease_node


def run():
    time.sleep(random.random() * 10)
    base_url = get_lease_node()
    resp = requests.get("http://" + base_url)
    # print(resp.text)


def main():
    while True:
        T = []
        for i in range(1000):
            T.append(Thread(target=run))

        for t in T:
            t.start()

        for t in T:
            t.join()
        time.sleep(random.random() * 100)


if __name__ == '__main__':
    main()
