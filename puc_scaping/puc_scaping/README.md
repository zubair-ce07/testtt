# PUC NY SCRAPPER
=======

## Instructions
 Run the spider with below command with required from and to date and output file name:

```sh
$ scrapy crawl docket -a from_date="12/11/2017" -a to_date="12/11/2017" -o dockets.json
```

- From and to date must be in **<MM/DD/YYYY>** from date
- From and to date must not be in future
- From date must not be greater than to date