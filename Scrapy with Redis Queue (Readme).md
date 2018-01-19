Scrapy with Redis Queue
=======

## Prerequisites:

1. Python 3.5 should be installed.
2. Scrapy should be installed.
3. Scutils should be installed.



## Writing items to Redis Queue:

Steps:

1. Install **Redis** using this [link](http://grainier.net/how-to-install-redis-in-ubuntu/).
2. After installing check that Redis server is up and running using command: **redis-cli ping** which must respond with **PONG**.
3. In application, to import Redis use: **import Redis**.

To create a connection with Redis:
redis_conn = Redis()

To create a queue with key “item”:
queue = RedisQueue(redis_conn, "item")

queue.push() and queue.pop() methods are used to enqueue and dequeue from queue respectively

----------------------------------------------------------------------------------------------------------------------------

To run sample project, open two terminal windows and go to project directory. First, run the following command in first terminal window:
**scrapy crawl orsay_links**

Second, run the following command in second terminal window:
**scrapy crawl orsay_products -o items.json**

What this sample project does is that spider **“orsay_links”** extract all the products links and push them in queue with a 2 seconds delay.
And other spider running will keep on checking that if anything (product url in our case) appears in queue it pops out and yield request to that url to scrape the product data and finally stores the data in file named items.json.
If nothing appears in queue then there is a delay of 2 seconds before checking the queue again








