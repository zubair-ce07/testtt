**Concurrent and Parallel**

Wikipedia Football World cup 2018

**Parallel**
1. Arguments to run file(optional)
   a. -p parallel threads to run(default = 5)
   b. -r max requests to process(default = 50)
2. start url = "https://en.wikipedia.org/wiki/2018_FIFA_World_Cup"
3. all the 'a' tags in the page are extracted
4. first to max_requests are processed by making threads to handle each
5. parallel_requests limit the number of threads

**Concurrent**
1. Arguments to run file(optional)
   a. -p parallel calls to run(default = 5)
   b. -r max requests to process(default = 50)
   c. -d dealy to wait for between 2 requests(default = 2)
2. start url = "https://en.wikipedia.org/wiki/2018_FIFA_World_Cup"
3. all the 'a' tags in the page are extracted
4. first to max_requests are processed by giving syncronus calls to request.get()
5. syncronus calls limited to parallel_requests
