import argparse
import asyncio
import requests
from parsel import Selector


async def get_links(url,timeout_):
    links = []
    response = requests.get(url,timeout=timeout_)
    sel = Selector(response.text)
    data =  sel.css(' a[href^="http"]::attr(href)  ')
    for link in data:
        links.append(link.extract())

    return links


async def get_result(url_list,index,count,max_urls,bytesdownloaded,timeout_):
    if index<len(url_list) and url_list[index] and count[0] < max_urls:
        links = await get_links(url_list[index],timeout_);
        for link in links:
            url_list.append(link)
        bytesdownloaded[0] += len(links)
        index += 1
        count[0] +=1
        await  get_result(url_list,index,count,max_urls,bytesdownloaded,timeout_)

async def print_report(url_list,index,count,max_urls,bytesdownloaded,timeout_):
    await  get_result(url_list, index, count, max_urls, bytesdownloaded, timeout_)
    if max_urls > len(url_list):
        max_urls = len(url_list)
    print("Total requests made are {0}".format(max_urls))
    print("Total bytes downloaded are {0}".format(bytesdownloaded[0]))
    print("Average size of a page is {0}".format(bytesdownloaded[0]/max_urls))
def main():
    links = []
    links.append('https://en.wikipedia.org/wiki/Constitution_of_Pakistan')

    parser = argparse.ArgumentParser(
        description='Script retrieves Commands from User')

    parser.add_argument(
        '-m', '--max_urls', type=str, help='Maximum Urls', required=True)

    parser.add_argument(
        '-d', '--delay', type=str, help='tolerate download delay', required=True)




    args = parser.parse_args()

    max_urls = int(args.max_urls)
    index = 0
    count = [0]
    bytesdownloaded = [0]
    timeout_ = int(args.delay)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_report(links, index, count, max_urls, bytesdownloaded, timeout_))
    loop.close()

if __name__ == "__main__":
    main()
