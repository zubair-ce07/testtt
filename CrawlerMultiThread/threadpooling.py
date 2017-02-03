#!/usr/bin/python3

import parsel
import requests
import asyncio
import os

nWorkers = 8
downloadDelay = 1/10
maxRequests = 150

q = asyncio.Queue()
baseUrl = 'http://www.bluefly.com'
doneUrls = []
totalRequests = 0
sizes = []
pids = []


async def url_worker(workerName, q):
    global totalRequests
    global doneUrls
    global sizes
    global pids
    while (q.empty() is False) and (totalRequests < maxRequests):
        url = await q.get()
        totalRequests += 1
        print(workerName, url, 'totalRequests: ', totalRequests)
        await asyncio.sleep(downloadDelay)
        response = requests.get(url)
        doneUrls.append(url)

        # await asyncio.sleep(downloadDelay)
        if response.status_code == 200:
            sel = parsel.Selector(response.text)
            refs = sel.xpath('//a/@href').extract()
            validLinks = getsuburls(url, refs)
            sizes.append(len(response.content))
            pids.append(workerName)
            for newlink in validLinks:
                q.put_nowait(newlink)
        else:
            print(response.status_code)

    return workerName


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


def main():
    print("\n*ThreadPooling*\n")
    loop = asyncio.get_event_loop()
    response = requests.get(baseUrl)
    print('Accessed url:', response.url)

    sel = parsel.Selector(response.text)
    refs = sel.xpath('//a/@href').extract()
    validLinks = getsuburls(baseUrl, refs)

    q.put_nowait(baseUrl)
    for link in validLinks[0:nWorkers-1]:
        q.put_nowait(link)

    print('\n****EXECUTING****\n')
    tasks = []
    # for i in range(0, nworkers):
    #     f.append(asyncio.Future())
    for i in range(0, nWorkers):
        tasks.append(asyncio.ensure_future(url_worker("worker"+str(i+1), q)))
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()

    print('\n****FINISHED****\n')
    print('totalRequests:', totalRequests)
    print('Workers: ', set(pids))
    print('Total Downloaded: ', sum(sizes))
    print('Avg Page Size: ', sum(sizes)/totalRequests)

    return


if __name__ == "__main__":
    os.system('clear')
    main()
