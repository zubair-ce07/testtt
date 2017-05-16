from parsel import Selector
import requests
import asyncio

THREAD_NUM = 15
DOWNLOAD_DELAY = 0.05
INPUT_URL = 'http://stackabuse.com/python-async-await-tutorial/'


def sanitize_url(url, input_url):
    """
    :param url: the provided url to sanitize  
    :param input_url: the input url provided by the user
    :return: returns the url if it's an external link and concatenated url if it is internal  
    """
    if url.startswith('http'):
        return url
    if input_url.endswith('/') and url.startswith('/'):
        url = url[1:]
    if not input_url.endswith('/') and not url.startswith('/'):
        input_url += '/'
    input_url = host_name_retrieval(input_url)
    return input_url + url


async def call_url(urls, delay, input_url):
    """ 
        :param delay: download delay specified by the user.
        :param input_url: The input URL provided by user
        :param urls: list of urls to crawl
        :returns list containing total data size and total number of urls 
                 processed    
    """
    data_size, urls_processed = 0, 0
    for url in urls:
        url = sanitize_url(url, input_url)
        response = await get_data_from_url(url, delay)
        if response:
            data = response.content
            data_size += len(data)
            urls_processed += 1
        else:
            print('{} on : {}'.format(response.status_code, url))
    return [data_size, urls_processed]


async def get_data_from_url(url, delay):
    await asyncio.sleep(delay)
    return requests.get(url)


def host_name_retrieval(url):
    """
    :param url: the input url from which hostname is to be extracted 
    :return: returns the hostname of this url
    """
    elements = url.split('/')
    return '{0}/{1}/{2}/'.format(elements[0], elements[1], elements[2])


def main():
    response = requests.get(INPUT_URL)
    raw_html = response.content
    sel = Selector(text=raw_html.decode('unicode-escape'))
    raw_urls = sel.xpath('.//a/@href').extract()
    # print(kpl for kpl in raw_urls)
    print(len(raw_urls))
    urls = [[] for i in range(THREAD_NUM)]
    url_iter = 0
    if THREAD_NUM > len(raw_urls):
        print('Fatal Error: Threads more than urls')
        return
    for i in range(len(raw_urls)):
        urls[url_iter].append(raw_urls[i])
        url_iter = 0 if url_iter == (THREAD_NUM - 1) else url_iter + 1
    co_routines = [call_url(urls[i], DOWNLOAD_DELAY, INPUT_URL) for i in range(THREAD_NUM)]
    loop = asyncio.get_event_loop()
    x = loop.run_until_complete(asyncio.wait(co_routines))
    data_sum = [0, 0]
    for e in x[0]:
        data_sum[0] += e.result()[0]
        data_sum[1] += e.result()[1]
    print('Total Bytes: {} Total Urls Processed: {} Average URL Size: {}'.format(data_sum[0],
                                                                                 data_sum[1], data_sum[0]/data_sum[1]))

if __name__ == '__main__':
    main()

