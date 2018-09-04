# Orsay

Scrapy project to scrape website and form json </br>
Python version: 3.6

## Problem Statement

Website: http://www.orsay.com/de-de/ </br>

You need to scrape it in order to get data of products. Sample data for a given product is as follows: </br>

```
{'brand': 'Orsay',
  'care': ['4% ELASTHAN, 96% POLYESTER'],
  'category': [],
  'description': ['Unser Tipp: Eleganter Look mit figurbetonter Ankle und '
                  'abgestimmten Blazer von ORSAY!'],
  'gender': 'women',
  'image_urls': ['http://images.orsay.com/media/catalog/product/cache/allstores/image/9df78eab33525d08d6e5fb8d27136e95/1/0/103068_97f.jpg',
                 'http://images.orsay.com/media/catalog/product/cache/allstores/image/9df78eab33525d08d6e5fb8d27136e95/1/0/103068_98f.jpg'],
 
  'name': ['Shoulder-Cut out Top'],
  'retailer_sku': '103068',
  'skus': {'10306897_L': {'colour': 'Schwarz',
                          'currency': 'EUR',
                          'price': 1599,
                          'size': 'L'},
           '10306897_M': {'colour': 'Schwarz',
                          'currency': 'EUR',
                          'price': 1599,
                          'size': 'M'},
           '10306897_S': {'colour': 'Schwarz',
                          'currency': 'EUR',
                          'price': 1599,
                          'size': 'S'},
           '10306897_XL': {'colour': 'Schwarz',
                           'currency': 'EUR',
                           'out_of_stock': True,
                           'price': 1599,
                           'size': 'XL'},
           '10306897_XS': {'colour': 'Schwarz',
                           'currency': 'EUR',
                           'price': 1599,
                           'size': 'XS'},
           '10306897_XXL': {'colour': 'Schwarz',
                            'currency': 'EUR',
                            'out_of_stock': True,
                            'price': 1599,
                            'size': 'XXL'},
           '10306897_XXS': {'colour': 'Schwarz',
                            'currency': 'EUR',
                            'out_of_stock': True,
                            'price': 1599,
                            'size': 'XXS'},
           '10306898_L': {'colour': 'Gelb',
                          'currency': 'EUR',
                          'price': 1599,
                          'size': 'L'},
           '10306898_M': {'colour': 'Gelb',
                          'currency': 'EUR',
                          'price': 1599,
                          'size': 'M'},
           '10306898_S': {'colour': 'Gelb',
                          'currency': 'EUR',
                          'price': 1599,
                          'size': 'S'},
           '10306898_XL': {'colour': 'Gelb',
                           'currency': 'EUR',
                           'out_of_stock': True,
                           'price': 1599,
                           'size': 'XL'},
           '10306898_XS': {'colour': 'Gelb',
                           'currency': 'EUR',
                           'price': 1599,
                           'size': 'XS'},
           '10306898_XXL': {'colour': 'Gelb',
                            'currency': 'EUR',
                            'out_of_stock': True,
                            'price': 1599,
                            'size': 'XXL'},
           '10306898_XXS': {'colour': 'Gelb',
                            'currency': 'EUR',
                            'out_of_stock': True,
                            'price': 1599,
                            'size': 'XXS'}},
  'url': 'http://www.orsay.com/de-de/shoulder-cut-out-top-10306897.html'}
```

Save all of that data in a json file. 
