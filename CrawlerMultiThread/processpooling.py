#!/usr/bin/python3

import parsel
import requests
from concurrent.futures import ProcessPoolExecutor, as_completed
import time
import os
import queue

nWorkers = 8
downloadDelay = 1/10
maxRequests = 150

q = queue.Queue()
baseUrl = 'http://www.bluefly.com'
doneUrls = []
totalRequests = 0
sizes = []
pids = []


def url_worker(url, numRequests):
    pid = os.getpid()
    print(pid, url, 'totalRequests: ', numRequests)
    time.sleep(downloadDelay)
    res = requests.get(url)
    # time.sleep(downloadDelay)
    validLinks = []
    if res.status_code == 200:
        sel = parsel.Selector(res.text)
        refs = sel.xpath('//a/@href').extract()
        validLinks = getsuburls(url, refs)
        return len(res.content), pid, validLinks
    else:
        return 0, pid, validLinks


def getsuburls(baselink, textLinks):
    subLinks = []
    linksDoneCounter = 0
    for link in textLinks:
        if not link.startswith('http') and (link.startswith('/') or link.startswith('?')):
            newLink = requests.compat.urljoin(baselink, link)
            if newLink not in doneUrls:
                if newLink not in subLinks:
                    subLinks.append(newLink)
            else:
                linksDoneCounter += 1
        # else:
        #     print('Excluded: ', link)

    # if linksDoneCounter > 0:
    #     print("Link already DONE: ", linksDoneCounter)

    return subLinks


def add_thread(myfutures, executor, link):
    global totalRequests
    global doneUrls
    if totalRequests >= maxRequests:
        return -1
    totalRequests += 1
    cur_future = executor.submit(url_worker, link, totalRequests)
    myfutures.append(cur_future)
    doneUrls.append(link)
    return 0


def main():
    print("\n*ProcessPooling*\n")
    pool = ProcessPoolExecutor(max_workers = nWorkers)

    q.put(baseUrl)
    print('\n****EXECUTING****\n')

    myfutures = []
    ret = 0
    while (q.empty() is False) and (ret >= 0):
        link = q.get()
        ret = add_thread(myfutures, pool, link)
        for cur_future in as_completed(myfutures):
            # print(cur_future.result(), time.ctime(time.time()), cur_future.done())
            myfutures.remove(cur_future)
            sizes.append(cur_future.result()[0])
            pids.append(cur_future.result()[1])
            for newLink in cur_future.result()[2]:
                q.put(newLink)

    print('\n****FINISHED****\n')
    print('totalRequests:', totalRequests)
    print('Workers: ', set(pids))
    print('Total Downloaded: ', sum(sizes))
    print('Avg Page Size: ', sum(sizes)/totalRequests)

    return


if __name__ == "__main__":
    os.system('clear')
    main()
