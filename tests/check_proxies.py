import threading
import queue

import requests

def check_proxy(proxy):
    try:
        res = requests.get('http://ipinfo.io/json', proxies={"http": proxy, "https": proxy})
        if res.status_code == 200:
            return True
        else:
            return False
    except:
        return False

def check_proxies():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            res = requests.get('http://ipinfo.io/json', proxies={"http": proxy, "https": proxy})
        except:
            continue
        if res.status_code == 200:
            print(proxy)


if __name__ == "__main__":

    q = queue.Queue()
    valid_proxies = []


    with open("proxies/proxy_list.txt", "r") as f:
        proxies = f.read().split('\n')
        for p in proxies:
            q.put(p)

    for _ in range(10):
        threading.Thread(target=check_proxies).start()