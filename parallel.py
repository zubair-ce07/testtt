import requests
from parsel import Selector
from urllib import parse
import asyncio
from concurrent import futures
from concurrent.futures import ProcessPoolExecutor, as_completed
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


def collect_data(u,download_delay):

    try:
        response_body = requests.get(u, timeout=30).text
        downloaded_bytes=len(response_body)

        return downloaded_bytes
    except:
        return 0

def request_sending(links, no_of_requests):

    results_list=[]
    list_futures=[]
    results=[]
    with ProcessPoolExecutor(max_workers=5) as pool:
        for l in links:
            fut = pool.submit(collect_data, l,0)
            list_futures.append(fut)


        for result in as_completed(list_futures):
            results_list.append(result)
            print(result)

      #  for f in results_list:
       #     results.append(f.result())

   # return results




def main():
    url = 'https://arbisoft.com'

    max_url=5
    no_of_requests=5
    download_delay=0
    results=[]
    links = collect_urls(url)
    request_sending(links,no_of_requests)



if __name__ == '__main__':
    main()
