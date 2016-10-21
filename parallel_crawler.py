__author__ = 'rabia'
import concurrent.futures
import requests
import time
from lxml import html


def generate_report(urls_data_list, total_bytes, total_requests, no_of_workers):
    print("\n---------------Report---------------------")
    for item in urls_data_list:
        print('%r page is %d bytes' % (item['url'], item['bytes']))

    print("\n\nTotal Requests made: " + str(total_requests))
    print("Total Bytes downloaded: " + str(total_bytes))
    average_size_of_page = total_bytes / total_requests
    print("Average size of Page: " + str(average_size_of_page))
    print("Max Workers: " + str(no_of_workers))


def get_url_data(url):
    response = requests.get(url)
    time.sleep(2)
    return response


def parallel_crawler(urls_list, no_of_workers):

    urls_data_list = []
    total_bytes = 0
    total_requests = 0

    with concurrent.futures.ProcessPoolExecutor(max_workers=no_of_workers) as executor:
        future_to_url = {executor.submit(get_url_data, url): url for url in urls_list}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            response = future.result()
            response_size = len(response.text)
            total_requests += 1
            total_bytes += response_size
            urls_data_list.append({'url': url, 'bytes': response_size})

        generate_report(urls_data_list, total_bytes, total_requests, no_of_workers)


def main():

    no_of_workers = input('Enter the number of processes: ')

    base_url = "https://en.wikipedia.org/wiki/Data_science"
    response = requests.get(base_url)
    raw_string = html.fromstring(response.text)
    urls = raw_string.xpath("/html/body//a[starts-with(@href,'/wiki/')]/@href")
    urls_list = ['https://en.wikipedia.org' + url for url in urls]
    urls_list = urls_list[:100]

    parallel_crawler(urls_list, int(no_of_workers))


if __name__ == "__main__":
    main()