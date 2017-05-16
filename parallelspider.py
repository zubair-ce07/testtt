from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ALL_COMPLETED
from concurrent.futures import wait
import argparse
from parsel import Selector
import requests
import time


def parsing_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("URL", help="The input URL")
    parser.add_argument("download_delay", help="download_delay that each worker will respect when making the requests")
    parser.add_argument("thread_num", help="number of concurrent requests that can be made")
    parser.add_argument("-m", "--max", action="store")
    return parser.parse_args()


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


def call_url(urls, delay, input_url):
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
        response = get_data_from_url(url, delay)
        if response:
            data = response.content
            data_size += len(data)
            urls_processed += 1
        else:
            print('Status Code: {} on : {}'.format(response.status_code, url))
    return [data_size, urls_processed]


def get_data_from_url(url, delay):
    """
    :param url: url specified from which data is to be fetched
    :param delay: delay which it waits before making the request 
    :return: returns the response from the url
    """
    time.sleep(delay)
    return requests.get(url)


def host_name_retrieval(url):
    """
    :param url: the input url from which hostname is to be extracted 
    :return: returns the hostname of this url
    """
    elements = url.split('/')
    return '{0}/{1}/{2}/'.format(elements[0], elements[1], elements[2])


def main(args):
    """
    :param args: Command Line arguments: URL, download_delay and thread_limit are required parameters 
    in the respective order whereas max_limit is an option parameter declared with -m option
    :return: returns to main
    """
    response = requests.get(args.URL)
    raw_html = response.content
    max_threads = int(args.thread_num)
    download_delay = float(args.download_delay)
    sel = Selector(text=raw_html.decode('unicode-escape'))
    raw_urls = sel.xpath('.//a/@href').extract()
    max_limit = int(args.max) if args.max else len(raw_urls)
    max_limit = len(raw_urls) if max_limit > len(raw_urls) else max_limit
    urls = [[] for i in range(max_threads)]
    url_iter = 0
    if max_threads > max_limit:
        print('Fatal Error: Threads more than urls/max_limit Please ensure '
              'thread_limit must be less than max_limit')
        return
    for i in range(max_limit):
        urls[url_iter].append(raw_urls[i])
        url_iter = 0 if url_iter == (max_threads - 1) else url_iter + 1
    with ProcessPoolExecutor(max_workers=max_threads) as executor:
        futures = dict((executor.submit(call_url, urls[k], download_delay, args.URL), k) for k in range(max_threads))
        result = wait(futures, timeout=None, return_when=ALL_COMPLETED)
    data_sum = [0, 0]
    for e in result[0]:
        data_sum[0] += e.result()[0]
        data_sum[1] += e.result()[1]
    print('Total Bytes: {} Total Urls Processed: {} Average URL Size: {}'
          .format(data_sum[0], data_sum[1], round(data_sum[0]/data_sum[1])))


if __name__ == '__main__':
    main(parsing_arguments())





