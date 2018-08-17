import requests
from parsel import Selector
from urllib import parse
import asyncio
url_list=[]


def collect_urls(url):
    text = requests.get(url, timeout=30).text
    selector = Selector(text=text)
    url_list=selector.css('a::attr(href)').getall()
    i=0
    while i != len(url_list)-1:
        url_list[i]=parse.urljoin(url , url_list[i])
        i+=1

    return url_list


async def collect_data(u,download_delay):
    await asyncio.sleep(download_delay)
    try:
        response_body = requests.get(u, timeout=30).text
        downloaded_bytes=len(response_body)

        return downloaded_bytes
    except:
        return 0

def request_sending(links, no_of_requests):
    loop = asyncio.get_event_loop()
    #future = asyncio.Future()
    task=[]
    results_list=[]


    for l in links:
        task.append(asyncio.ensure_future(collect_data(l,0)))
        results_list=(loop.run_until_complete(asyncio.gather(*task)))
    loop.close()
    return results_list

def results_calculation(results):
    total_no_of_bytes=0
    for i in results:
        total_no_of_bytes=total_no_of_bytes+i
    return total_no_of_bytes


def main():
    url = 'https://arbisoft.com'

    max_url=5
    no_of_requests=5
    download_delay=0
    results=[]
    links = collect_urls(url)
    results=request_sending(links,no_of_requests)

    print('total number of requests made= ' +str(len(results)))
    print('Total bytes downloaded= ' +str(results_calculation(results))+ ' bytes')
    print('Average size of a page= ' +str((results_calculation(results))/len(results))+ ' bytes')
if __name__ == '__main__':
    main()
