import requests
import asyncio
import sys
from concurrent import futures
from parsel import Selector


async def concurrent_crawl(url):
        await asyncio.sleep(0.001)
        response = requests.get(url)
        return response

def parallel_crawl(url):
    response = requests.get(url)
    return response

async def concurrent_crawling(urls):
    tasks = []
    for url in urls:
        coro = concurrent_crawl(url)
        tasks.append(asyncio.ensure_future(coro))
        await asyncio.gather(*tasks)

    return tasks

def get_a_href(mainurl,no_of_urls):
    html_page = Selector(requests.get(mainurl).text)
    urls = html_page.xpath('//a').xpath("@href").getall()
    urls = [url for url in urls if ('https://' or 'http://') in url]
    urls = urls[0:no_of_urls]
    return urls

def start_concurrent_crawling(mainurl, no_of_urls_to_crawl):
    urls = get_a_href(mainurl,no_of_urls_to_crawl)
    loop = asyncio.get_event_loop()
    tasks = loop.run_until_complete(concurrent_crawling(urls))
    loop.close()

    len_sum = 0
    for task in tasks:
        len_sum += len(task.result().text)
    print()
    print("Total Number of Requests: "+str(no_of_urls_to_crawl))
    print("Total Bytes Downloaded: "+str(len_sum))
    print("Average size of page: "+str(len_sum/no_of_urls_to_crawl))
    print()

def start_parallel_crawling(mainurl, no_of_urls_to_crawl, no_of_process):
    urls = get_a_href(mainurl,no_of_urls_to_crawl)
    responses = []
    with futures.ProcessPoolExecutor(no_of_process) as executor:
        for response in executor.map(parallel_crawl,urls):
            responses.append(response)
    len_sum = 0
    for response in responses:
        len_sum += len(response.text)
    print()
    print("Total Number of Requests: "+str(no_of_urls_to_crawl))
    print("Total Bytes Downloaded: "+str(len_sum))
    print("Average size of page: "+str(len_sum/no_of_urls_to_crawl))
    print()

def start_concurrent():
    main_urls = input("Enter main url : ")
    no_of_urls_to_crawl = int(input("Enter no. of link to crawl : "))
    start_concurrent_crawling(main_urls,no_of_urls_to_crawl)

def start_parallel():
    main_urls = input("Enter main url : ")
    no_of_urls_to_crawl = int(input("Enter no. of link to crawl : "))
    no_of_prcesses = int(input("Enter no of processes to make : "))
    start_parallel_crawling(main_urls,no_of_urls_to_crawl,no_of_prcesses)
    

def show_menu():
    print("press 1 to concurrent crawling")
    print("press 2 to Parallel crawling")
    print("press e to Exit")

def start():
    while True:
        show_menu()
        option = input("Enter Your Choice : ")
        if option == "1":
            start_concurrent()
        elif option == "2":
            start_parallel()
        elif option == "e":
            sys.exit(0)

start()
