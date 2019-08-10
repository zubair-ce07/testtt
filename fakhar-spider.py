import aiohttp
import requests
import asyncio
import argparse
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from parsel import Selector

URLS_VISITED = 0
TOTAL_PAGE_SIZE = 0
TOTAL_REQUESTS = 0


def parse_arguments():
    # ----------- ADDING ARGUMENTS TO ARGUMENT PARSER ---------------#
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--requests", type=int, default=1, dest="requests",
                        help="Concurrent requests to make")
    parser.add_argument("-d", "--delay",
                        type=int, default=1, dest="delay", help="Download delay (Default : 1s)")
    parser.add_argument("-u", "--urls", type=int, default=0, dest="number_urls_visit",
                        help="Number of URLs to visit")
    # -----------/ ADDING ARGUMENTS TO ARGUMENT PARSER / ---------------#
    # ----------- Parsing Command Line Arguments to Parse --------------#
    return parser.parse_args(sys.argv[1:])


class FakharSpiderConcurrent:
    def __init__(self, arguments):
        self._download_delay = arguments.delay
        self._urls_to_visit = arguments.number_urls_visit
        self._requests = arguments.requests

    @staticmethod
    async def get_urls(content):
        return content.xpath("//a/@href").getall()

    @staticmethod
    async def get_general_images(content):
        return content.xpath("//source/@srcset").getall()

    @staticmethod
    async def get_item_images(content):
        return content.xpath("//img/@src").getall()

    @staticmethod
    async def get_text(content):
        return content.xpath(
            "//body//*[self::span or self::div or self::p or self::a or self::h2 or self::li]//text()").getall()

    @staticmethod
    def correct_url_and_text(urls, text):
        return list(set(urls)), [item for item in text if len(item) > 2]

    @staticmethod
    def append_parent_address_url(website, urls):
        corrected_urls = []
        for url in urls:
            if "http" not in url:
                corrected_urls.append("".join(f"{website}{url}"))
        return corrected_urls

    @staticmethod
    def print_retrieved_data(website, urls, item_images, general_images, text):
        for link in urls:
            print(f"{website} :: Link Found : {link}", end="\n")
        for img_src in item_images:
            print(f"{website} :: Product Image Found : {img_src}", end="\n")
        for images in general_images:
            print(f"{website} :: Card Image Found : {images}", end="\n")
        for item in text:
            if item == "\n":
                continue
            else:
                print(f"{website} :: Text Found : {item}", end="\n")

    async def make_requests(self, client, website):
        async with client.get(website) as response:
            global TOTAL_REQUESTS

            print(
                f"Link : {website} :: having a download delay of : {self._download_delay} s")
            # ------------------ Awaiting for the Delay user Specified --------------------------#
            await asyncio.sleep(self._download_delay)
            website_html = await response.read()

            TOTAL_REQUESTS += 1
            content = Selector(str(website_html))
            # ---------------- Crawling the link for urls, images ----------------------#
            urls = await self.get_urls(content)
            general_images = await self.get_general_images(content)
            item_images = await self.get_item_images(content)
            text = await self.get_text(content)
            # ---------------- Removing duplicate Links / Spaces from Text ----------------------#
            urls, corrected_text = self.correct_url_and_text(urls, text)
            # ----------------- Joining parent address where not stored -----------------#
            corrected_urls = self.append_parent_address_url(website, urls)
            # ---------------- Displaying URLS, IMAGES and TEXT ----------------------#
            self.print_retrieved_data(
                website, corrected_urls, item_images, general_images, corrected_text)
            # ---------------- Visiting -u URLS found from the website -------------------#
            global URLS_VISITED
            global TOTAL_PAGE_SIZE
            if URLS_VISITED != self._urls_to_visit:
                # ---------------------- Making -u urls as TASKS ------------------------#
                visit_url_tasks = [asyncio.ensure_future(self.make_requests(client, corrected_urls[count])) for count in
                                   range(
                                       self._urls_to_visit - URLS_VISITED + 1) if count > 0]
                # ---------------------- Tasks Created = Urls to Visit -----------------------#
                URLS_VISITED += len(visit_url_tasks)

                # ---------------------- Asyncronously calling Tasks -----------------------#
                '''----------------LOGIC : URL to visit must only be run, which are specified by the user--------------
                   ---------------- 5 urls to visit, suer specifies 2 concurrent requests to be made ------------------
                   ---------------- so 2 urls should make requests, the rest 3 should await. and likewise. --------- '''
                visit = 0
                tasks_to_run = []
                returned_urls = []
                returned_url_page_size = []
                # ---------------- Run while, (NUMBER OF URL) times --------------------#
                while visit != len(visit_url_tasks):
                    tasks_to_run.clear()
                    # --------------- Gather -r(CONCURRENT REQUESTS) tasks from total list of -u(URLS TO VISIT) ------#

                    for _ in range(self._requests):
                        if visit == len(visit_url_tasks):
                            break
                        tasks_to_run.append(visit_url_tasks[visit])
                        visit += 1
                    # --------------- Run the new batch of tasks ---------------------#
                    done, _ = await asyncio.wait(tasks_to_run) if len(
                        tasks_to_run) > 0 else None
                    for task_id, task in enumerate(visit_url_tasks):
                        if task in done:
                            returned_urls.append(corrected_urls[task_id + 1])
                            returned_url_page_size.append(task.result())
                            TOTAL_PAGE_SIZE += task.result()

                for index in range(len(returned_urls)):
                    print(
                        f"""URL: {returned_urls[index]}:: Average Page Size : {TOTAL_PAGE_SIZE / self._urls_to_visit}
                         :: Page Size : {returned_url_page_size[index]} """)

            return len(website_html)


class FakharSpiderParallel:
    def __init__(self, arguments):
        self._download_delay = arguments.delay
        self._urls_to_visit = arguments.number_urls_visit
        self._requests = arguments.requests

    @staticmethod
    def get_urls(content):
        return content.xpath("//a/@href").getall()

    @staticmethod
    def get_general_images(content):
        return content.xpath("//source/@srcset").getall()

    @staticmethod
    def get_item_images(content):
        return content.xpath("//img/@src").getall()

    @staticmethod
    def get_text(content):
        return content.xpath(
            "//body//*[self::span or self::div or self::p or self::a or self::h2 or self::li]//text()").getall()

    @staticmethod
    def correct_url_and_text(urls, text):
        return list(set(urls)), [item for item in text if len(item) > 2]

    @staticmethod
    def append_parent_address_url(website, urls):
        corrected_urls = []
        for url in urls:
            if "http" not in url:
                corrected_urls.append("".join(f"{website}{url}"))
        return corrected_urls

    @staticmethod
    def print_retrieved_data(website, urls, item_images, general_images, text):
        for link in urls:
            print(f"{website} :: Link Found : {link}", end="\n")
        for img_src in item_images:
            print(f"{website} :: Product Image Found : {img_src}", end="\n")
        for images in general_images:
            print(f"{website} :: Card Image Found : {images}", end="\n")
        for item in text:
            if item == "\n":
                continue
            else:
                print(f"{website} :: Text Found : {item}", end="\n")

    def make_requests(self, website):
        global TOTAL_REQUESTS
        print(f"{website} :: GOING TO SLEEP FOR {self._download_delay} s")
        time.sleep(self._download_delay)
        response = requests.get(website)
        website_html = response.text
        TOTAL_REQUESTS += 1
        content = Selector(str(website_html))
        # ---------------- Crawling the link for urls, images ----------------------#
        urls = self.get_urls(content)
        general_images = self.get_general_images(content)
        item_images = self.get_item_images(content)
        text = self.get_text(content)
        # ---------------- Removing duplicate Links / Spaces from Text ----------------------#
        urls, corrected_text = self.correct_url_and_text(urls, text)
        # ----------------- Joining parent address where not stored -----------------#
        corrected_urls = self.append_parent_address_url(website, urls)
        # ---------------- Displaying URLS, IMAGES and TEXT ----------------------#
        self.print_retrieved_data(
            website, corrected_urls, item_images, general_images, corrected_text)
        # ---------------- Visiting -u URLS found from the website -------------------#
        global URLS_VISITED
        global TOTAL_PAGE_SIZE
        if URLS_VISITED != self._urls_to_visit:
            # ---------------------- Making -u urls as TASKS, +1 because the first link is always the home page -------#
            visit_url_tasks = [corrected_urls[url + 1]
                               for url in range(self._urls_to_visit)]
            # ---------------------- Tasks Created = Urls to Visit -----------------------#
            URLS_VISITED += len(visit_url_tasks)
            # ---------------------- Parallel calling Tasks -----------------------#
            returned_urls = []
            returned_url_download_size = []
            with ThreadPoolExecutor(max_workers=self._urls_to_visit) as executor:
                # ------------- Making threads to execute -------------------#
                future_to_url = {executor.submit(
                    self.make_requests, url): url for url in visit_url_tasks}
                for future in as_completed(future_to_url):
                    url = future_to_url[future]
                    data = future.result()
                    returned_urls.append(url)
                    returned_url_download_size.append(len(data[1]))
                    TOTAL_PAGE_SIZE += len(data[0]
                                           ) if len(data[0]) > 0 else 0
                # --------------- Calclating Average of each URL Page ---------------------#
                for index in range(len(returned_urls)):
                    print(
                        f"""URL: {returned_urls[index]}:: Average Page Size : {TOTAL_PAGE_SIZE / self._urls_to_visit}
                                                    :: Download Size : {returned_url_download_size[index]}""")
        # ------ When crawling is complete, return page size and download size -------------#
        return [website_html, response.content]


async def concurrent_call(loop, arguments):
    client = aiohttp.ClientSession(loop=loop)
    spider = FakharSpiderConcurrent(arguments)
    # --------------- Making Tasks for requesting webpage -r times specified by user ------------------#
    task = [asyncio.ensure_future(
        spider.make_requests(client, "https://www.target.com"))]

    # --------------- Requesting the website, and awaiting on the task to complete ------------------#
    done, _ = await asyncio.wait(task)

    # --------------- for each task which is completed, do the following ------------------#
    # for task in tasks:
    #    if task in done:
    #        print("DONE")
    await client.close()


def main():
    global URLS_VISITED
    global TOTAL_PAGE_SIZE
    global TOTAL_REQUESTS

    arguments = parse_arguments()
    start = time.time()
    # ----- CONCURRERNT SPIDER ---------#
    loop = asyncio.get_event_loop()
    loop.run_until_complete(concurrent_call(loop, arguments))
    loop.stop()
    end = time.time()

    print(f"Time Took to Crawl CONCURRENTLY : {end - start}")
    print(f"Total requests made : {TOTAL_REQUESTS}")
    # ------------- Reinitializing values of global variables to 0 ---------#
    URLS_VISITED = TOTAL_PAGE_SIZE = TOTAL_REQUESTS = 0
    time.sleep(5)

    start = time.time()
    # ----- PARALLEL SPIDER ---------#
    spider = FakharSpiderParallel(arguments)
    # --------------- Making Tasks for requesting web page -r times specified by user ------------------#
    spider.make_requests("https://www.target.com"),
    end = time.time()
    print(f"Time Took to Crawl PARALLEL : {end - start}")
    print(f"Total requests made : {TOTAL_REQUESTS}")


if __name__ == "__main__":
    main()
