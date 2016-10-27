import asyncio
from parsel import Selector
from queue import Queue
import aiohttp


async def crawl(domain, max_urls=20, delay=1):
    urls_q = asyncio.Queue()
    visited = set()
    size = 0

    urls_q.put_nowait(domain)
    while not urls_q.empty() or len(visited) > max_urls:
        url = await urls_q.get()
        if url not in visited:
            visited.add(url)
            url_size, new_urls = await visit(url)

            size = size + url_size
            for new_url in new_urls:
                new_url = domain + new_url
                if new_url not in visited:
                    urls_q.put_nowait(new_url)
        asyncio.sleep(delay)


async def visit(url):
    print(url)
    try:
        resp = await aiohttp.request('GET', url)
        body = await resp.read()
        size = len(body)
        urls = get_urls(body.decode('utf-8'))
        return (size, urls)
    except Exception as exc:
        print("Warning: (%s) url skipped due to error" % url)
        print(str(exc))
        return (0, [])


def get_urls(body):
    sel = Selector(text=body)
    return sel.xpath('//a//@href').extract()

if __name__ == "__main__":

    domain = "https://www.arbisoft.com"

    loop = asyncio.get_event_loop()
    tasks = [crawl(domain)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
