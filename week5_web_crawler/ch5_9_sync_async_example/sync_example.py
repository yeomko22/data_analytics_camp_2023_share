import time
import random


def remote_request():
    time.sleep(1)
    return random.randint(0, 10)


def sync_crawl():
    result = []
    for i in range(10):
        resp = remote_request()
        result.append(resp)
    print(result)


if __name__ == '__main__':
    sync_crawl()
