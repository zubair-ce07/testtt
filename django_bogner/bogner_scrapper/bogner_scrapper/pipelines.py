# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from products.models import Product, Category


class BognerScrapperPipeline(object):
    def process_item(self, item, spider):
        try:
            product = Product.objects.get(retailer_sku=item['retailer_sku'])
            return item
        except(KeyError, Product.DoesNotExist):
            self.add_categories(item)
            product = Product(url=item['url'], retailer_sku=item['retailer_sku'], brand=item['brand'],
                              gender=item['gender'], name=item['name'], description=item['description'],
                              care=item['care'], image_urls=item['image_urls'], market=item['market'],
                              retailer=item['retailer'], skus=item['skus'], price=item['price'],
                              currency=item['currency'])
            product.save()
            for cat in item['category']:
                print(cat)
                category = Category.objects.get(category_name=cat)
                product.category.add(category)
            return item

    def add_categories(self, item):
        for cat in item['category']:
            try:
                category = Category.objects.get(category_name=cat)
            except(KeyError, Category.DoesNotExist):
                category = Category(category_name=cat)
                category.save()
