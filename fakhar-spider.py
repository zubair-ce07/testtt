import aiohttp
import requests
import asyncio
import argparse
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from parsel import Selector

urls_visited = 0
total_page_size = 0
total_requests_made = 0


class FakharSpider:
    def __init__(self):
        self._download_delay = None
        self._urls_to_visit = None
        self._concurrent_requests = None

    def parse_arguments(self):
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
        arguments = parser.parse_args(sys.argv[1:])
        # ----------- / Parsing Command Line Arguments to Parse / --------------#
        self._concurrent_requests = arguments.requests
        self._download_delay = arguments.delay
        self._urls_to_visit = arguments.number_urls_visit

    async def get_urls_concurrent(self, content):
        return content.xpath("//a/@href").getall()

    async def get_general_images_concurrent(self, content):
        return content.xpath("//source/@srcset").getall()

    async def get_item_images_concurrent(self, content):
        return content.xpath("//img/@src").getall()

    async def get_text_concurrent(self, content):
        return content.xpath(
            "//body//*[self::span or self::div or self::p or self::a or self::h2 or self::li]//text()").getall()

    @staticmethod
    def get_urls_parallel(content):
        return content.xpath("//a/@href").getall()

    @staticmethod
    def get_general_images_parallel(content):
        return content.xpath("//source/@srcset").getall()

    @staticmethod
    def get_item_images_parallel(content):
        return content.xpath("//img/@src").getall()

    @staticmethod
    def get_text_parallel(content):
        return content.xpath(
            "//body//*[self::span or self::div or self::p or self::a or self::h2 or self::li]//text()").getall()

    async def make_requests_in_concurrent(self, client, website):
        async with client.get(website) as response:
            global total_requests_made
            print(
                f"Link : {website} :: having a download delay of : {self._download_delay} s")
            # ------------------ Awaiting for the Delay user Specified --------------------------#
            await asyncio.sleep(self._download_delay)
            website_html = await response.read()
            total_requests_made += 1
            content = Selector(str(website_html))
            # ---------------- Crawling the link for urls, images ----------------------#
            urls = await self.get_urls_concurrent(content)
            general_images = await self.get_general_images_concurrent(content)
            item_images = await self.get_item_images_concurrent(content)
            text = await self.get_text_concurrent(content)
            # ---------------- Removing duplicate Links / Spaces from Text ----------------------#
            urls, corrected_text = self.correct_url_and_text(urls, text)
            # ----------------- Joining parent address where not stored -----------------#
            corrected_urls = self.append_parent_adress_url(website, urls)
            # ---------------- Displaying URLS, IMAGES and TEXT ----------------------#
            self.print_retrieved_data(
                website, corrected_urls, item_images, general_images, corrected_text)
         # ---------------- Visiting -u URLS found from the website -------------------#
            global urls_visited
            global total_page_size
            if urls_visited != self._urls_to_visit:
                # ---------------------- Making -u urls as TASKS ------------------------#
                visit_url_tasks = [asyncio.ensure_future(self.make_requests_in_concurrent(client, corrected_urls[count])) for count in
                                   range(
                                       self._urls_to_visit - urls_visited + 1) if count > 0]
                # ---------------------- Tasks Created = Urls to Visit -----------------------#
                urls_visited += len(visit_url_tasks)
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
                    for _ in range(self._concurrent_requests):
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
                            total_page_size += task.result()

                for index in range(len(returned_urls)):
                    print(
                        f"""URL: {returned_urls[index]}:: Average Page Size : {total_page_size / self._urls_to_visit}
                         :: Page Size : {returned_url_page_size[index]} """)

            return len(website_html)

    @staticmethod
    def correct_url_and_text(urls, text):
        return list(set(urls)), [item for item in text if len(item) > 2]

    @staticmethod
    def append_parent_adress_url(website, urls):
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

    def make_requests_in_parallel(self, website):
        global total_requests_made
        print(f"{website} :: GOING TO SLEEP FOR {self._download_delay} s")
        time.sleep(self._download_delay)
        response = requests.get(website)
        website_html = response.text

        total_requests_made += 1
        content = Selector(str(website_html))
        # ---------------- Crawling the link for urls, images ----------------------#
        urls = self.get_urls_parallel(content)
        general_images = self.get_general_images_parallel(content)
        item_images = self.get_item_images_parallel(content)
        text = self.get_text_parallel(content)
        # ---------------- Removing duplicate Links / Spaces from Text ----------------------#
        urls, corrected_text = self.correct_url_and_text(urls, text)
        # ----------------- Joining parent address where not stored -----------------#
        corrected_urls = self.append_parent_adress_url(website, urls)
        # ---------------- Displaying URLS, IMAGES and TEXT ----------------------#
        self.print_retrieved_data(
            website, corrected_urls, item_images, general_images, corrected_text)
        # ---------------- Visiting -u URLS found from the website -------------------#
        global urls_visited
        global total_page_size
        if urls_visited != self._urls_to_visit:
            # ---------------------- Making -u urls as TASKS, +1 because the first link is always the home page -------#
            visit_url_tasks = [corrected_urls[url + 1]
                               for url in range(self._urls_to_visit)]
            # ---------------------- Tasks Created = Urls to Visit -----------------------#
            urls_visited += len(visit_url_tasks)
            # ---------------------- Parallel calling Tasks -----------------------#
            returned_urls = []
            returned_url_download_size = []
            with ThreadPoolExecutor(max_workers=self._urls_to_visit) as executor:
                #------------- Making threads to execute -------------------#
                future_to_url = {executor.submit(
                    self.make_requests_in_parallel, url): url for url in visit_url_tasks}
                for future in as_completed(future_to_url):
                    url = future_to_url[future]
                    data = future.result()
                    returned_urls.append(url)
                    returned_url_download_size.append(len(data[1]))
                    total_page_size += len(data[0]) if len(data[0]) > 0 else 0
                # --------------- Calclating Average of each URL Page ---------------------#
                for index in range(len(returned_urls)):
                    print(
                        f"""URL: {returned_urls[index]}:: Average Page Size : {total_page_size / self._urls_to_visit}
                                                    :: Download Size : {returned_url_download_size[index]}""")

        # ------ When crawling is complete, return page size and download size -------------#
        return [website_html, response.content]


async def concurrent_call(loop):
    client = aiohttp.ClientSession(loop=loop)
    spider = FakharSpider()
    spider.parse_arguments()
    # --------------- Making Tasks for requesting webpage -r times specified by user ------------------#
    task = [asyncio.ensure_future(
        spider.make_requests_in_concurrent(client, "https://www.target.com"))]

    # --------------- Requesting the website, and awaiting on the task to complete ------------------#
    done, _ = await asyncio.wait(task)

    # --------------- for each task which is completed, do the following ------------------#
    # for task in tasks:
    #    if task in done:
    #        print("DONE")
    await client.close()


def call_concurrent_spider():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(concurrent_call(loop))
    loop.stop()


def call_parallel_spider():
    spider = FakharSpider()
    spider.parse_arguments()
    # --------------- Making Tasks for requesting webpage -r times specified by user ------------------#
    spider.make_requests_in_parallel("https://www.target.com"),


def main():
    global urls_visited
    global total_page_size
    global total_requests_made

    start = time.time()
    call_concurrent_spider()
    end = time.time()
    print(f"Time Took to Crawl CONCURRENTLY : {end - start}")
    print(f"Total requests made : {total_requests_made}")
    #------------- Reintitalizing values of global variables to 0 ---------#
    urls_visited = total_page_size = total_requests_made = 0
    time.sleep(5)

    start = time.time()
    call_parallel_spider()
    end = time.time()
    print(f"Time Took to Crawl PARALLEL : {end - start}")
    print(f"Total requests made : {total_requests_made}")


if __name__ == "__main__":
    main()
