from parsel import Selector
import requests
import asyncio

THREAD_NUM = 7
DOWNLOAD_DELAY = 0.05
INPUT_URL = 'http://stackabuse.com/python-async-await-tutorial/'


async def call_url(threadid, urls, delay):
    """ :argument urls: list of urls to crawl
        :argument delay: download delay specified by the user.
        :returns list containing total data size and total number of urls 
                 processed    
    """

    print('threadID: {}, {}, URLS: {}'.format(threadid, len(urls), urls))
    data_size, urls_processed = 0, 0
    for url in urls:
        try:
            url = url if 'http' in url else INPUT_URL+url
            response = await get_data_from_url(url, delay)
            data = response.content
            data_size += len(data)
            urls_processed += 1
        except:
            print("url: "+ url)
    print('Thread Completed: {}'.format(threadid))
    return [threadid, data_size, urls_processed]


async def get_data_from_url(url, delay):
    await asyncio.sleep(delay)
    return requests.get(url)


def main():
    response = requests.get(INPUT_URL)
    raw_html = response.content
    sel = Selector(text=raw_html.decode('unicode-escape'))
    raw_urls = sel.xpath('.//a/@href').extract()
    print(len(raw_urls))
    urls = [[] for i in range(THREAD_NUM)]
    url_iter = 0
    for i in range(len(raw_urls)):
        urls[url_iter].append(raw_urls[i])
        url_iter = 0 if url_iter == (THREAD_NUM - 1) else url_iter + 1
    futures = [call_url(i ,urls[i], DOWNLOAD_DELAY) for i in range(THREAD_NUM)]

    loop = asyncio.get_event_loop()
    x = loop.run_until_complete(asyncio.wait(futures))
    data_sum = [0 , 0]
    for e in x[0]:
        data_sum[0] += e.result()[1]
        data_sum[1] += e.result()[2]
    print('Total Bytes: {} Total Urls Processed: {} Average URL Size: {}'.format(data_sum[0], data_sum[1], data_sum[0]/data_sum[1]))
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(call_url())
    # r = requests.get('http://stackoverflow.com')
    # x = r.content
    # sel = Selector(text=x.decode('unicode-escape'))
    # urls = sel.xpath('.//a/@href').extract()
    # print(len(urls))
    # print(urls)


if __name__ == '__main__':
    main()

