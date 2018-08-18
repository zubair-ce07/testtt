import requests
from parsel import Selector
from urllib import parse
import asyncio
import argparse
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
    new_links=[]
    global download_delay

    if len(links)<no_of_requests:
        for l in links:
            task.append(asyncio.ensure_future(collect_data(l,download_delay)))
            results_list=(loop.run_until_complete(asyncio.gather(*task)))
    else:
        while links!=[]:
            new_links=links[0:no_of_requests]
            links=links[no_of_requests+1:len(links)-1]
            print(new_links)
            temp_results_list=[]
            for l in new_links:
                task.append(asyncio.ensure_future(collect_data(l, 0)))
                temp_results_list = (loop.run_until_complete(asyncio.gather(*task)))
            results_list=results_list+temp_results_list

    loop.close()
    return results_list

def results_calculation(results):
    total_no_of_bytes=0
    for i in results:
        total_no_of_bytes=total_no_of_bytes+i
    return total_no_of_bytes


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str, help='Enter the base URL you want to crawl')
    parser.add_argument('no_of_requests', type=int, help="Enter the number of concurrent requests you want to make")
    parser.add_argument('max_url', type=int, help="Enter the number of maximum URL's you want to visit")
    parser.add_argument('download_delay',type=int, help="Enter the delay you want to respect during concurrent requests")
    args = parser.parse_args()
    url=args.url
    max_url= args.max_url
    no_of_requests=args.no_of_requests
    download_delay=args.download_delay
    results=[]
    links = collect_urls(url)
    print('full:        ')
    print(links)
    results=request_sending(links,no_of_requests)

    print('total number of requests made= ' +str(len(results)))
    print('Total bytes downloaded= ' +str(results_calculation(results))+ ' bytes')
    print('Average size of a page= ' +str((results_calculation(results))/len(results))+ ' bytes')
if __name__ == '__main__':
    main()
