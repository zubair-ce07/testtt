import re
import json
from datetime import date, timedelta
import json
import requests
from lxml import html
from peewee import *

db = SqliteDatabase('price_notif.db')


class Item(Model):
    item_id = CharField()
    item_name = CharField()
    creation_date = DateField(default=date.today)
    price = CharField()
    currency = CharField()
    site_name = CharField()
    url = CharField()

    class Meta:
        database = db


class ItemSelector:
    price_xpath = ''
    name_xpath = ''
    price_css = ''
    site = ''

    def clean_name(self, name):
        return name

    def clean_price(self, price):
        return price

    def clean_currency(self, currency):
        return currency


class LipsyItemSelector(ItemSelector):
    price_xpath = '//*[@itemprop="price"]/@content'
    name_xpath = '//*[@id="titleDesc"]/*[@itemprop="name"]/text()'
    currency_xpath = '//*[@itemprop="priceCurrency"]/@content'


class AldoItemSelector(ItemSelector):
    price_xpath = '//*[@property="product:price:amount"]/@content'
    currency_xpath = '//*[@property="product:price:currency"]/@content'
    name_xpath = '//*[contains(@class,"product-title")]/span/text()'

    def clean_price(self, price):
        return re.findall('([\d\.]+)', price)[0]


class HtmlParser:
    response = None
    url = None

    def fetch(self, url):
        self.url = url
        r = requests.get(url)
        self.response = html.fromstring(r.content)

    def parse_item(self, item_selector, item_id, site_name):
        item = Item()
        item.item_id = item_id
        item.url = self.url
        name = self.response.xpath(item_selector.name_xpath)[0]
        item.item_name = item_selector.clean_name(name)

        price = self.response.xpath(item_selector.price_xpath)[0]
        item.price = item_selector.clean_price(price)

        currency = self.response.xpath(item_selector.currency_xpath)[0]
        item.currency = item_selector.clean_currency(currency)

        item.site_name = site_name
        return item


class DBHelper:
    def __init__(self):
        db.connect()
        Item.create_table(True)

    def add_item(self, item):
        if not Item.select().where(Item.item_id == item.item_id,
                                   Item.site_name == item.site_name,
                                   Item.creation_date == item.creation_date).count():
            item.save()

    def to_dict(self, raw_items):
        items = {}
        for raw_item in raw_items:
            item = {}
            item['name'] = raw_item.item_name
            item['site_name'] = raw_item.site_name
            item['item_id'] = raw_item.item_id
            item['price'] = raw_item.price
            item['currency'] = raw_item.currency
            item['creation_date'] = raw_item.creation_date
            item['url'] = raw_item.url
            item_key = item['item_id'] + item['site_name']
            items[item_key] = item

        return items

    def get_items(self, item_date):
        items = Item.select().where(Item.creation_date == item_date).execute()
        return self.to_dict(items)

    def get_additions(self):
        yest_items = self.get_items(date.today() - timedelta(1))
        today_items = self.get_items(date.today())

        items = []
        for item_key, item in today_items.items():
            if item_key not in yest_items:
                items += [item]

        return items

    def get_deletions(self):
        yest_items = self.get_items(date.today() - timedelta(1))
        today_items = self.get_items(date.today())

        items = []
        for item_key, item in yest_items.items():
            if item_key not in today_items:
                items += [item]

        return items

    def get_price_changes(self):
        yest_items = self.get_items(date.today() - timedelta(1))
        today_items = self.get_items(date.today())

        items = []
        for item_key, item in yest_items.items():
            item2 = today_items.get(item_key)
            if item2 and item['price'] != item2['price']:
                item['old_price'] = item2['price']
                items += [item]

        return items


def crawl(db_helper):
    aldo_item_selector = AldoItemSelector()
    lispy_item_selector = LipsyItemSelector()
    parser = HtmlParser()

    with open('input.json') as json_data:
        products = json.load(json_data)
        for product in products:
            id = product['id']
            for item in product['items']:
                print("Looking data for: ", item['url'])
                site_name = item['site_name']
                item_selector = lispy_item_selector if site_name == 'lipsy' else aldo_item_selector
                parser.fetch(item['url'])
                item = parser.parse_item(item_selector, id, site_name)
                db_helper.add_item(item)


def print_items(items):
    for item in items:
        raw_text = 'item id: ' + item['item_id']
        raw_text += '\n\tsite name: ' + item['site_name']
        raw_text += '\n\titem name: ' + item['name']
        raw_text += '\n\tprice: ' + item['price']
        raw_text += '\n\turl: ' + item['url']
        if item.get('old_price'):
            raw_text += '\n\tprevious_price: ' + item['pold_price']

        print(raw_text)


def generate_reports(db_helper):
    items = db_helper.get_additions()
    if items:
        print("\nNew items added today:")
        print_items(items)
    else:
        print ("\n No new additions")

    items = db_helper.get_deletions()
    if items:
        print("\nItems deleted today:")
        print_items(items)
    else:
        print ("\n No deletions today")

    items = db_helper.get_price_changes()
    if items:
        print("\nPrice changed for these items today:")
        print_items(items)
    else:
        print ("\n No price changes")


def main():
    db_helper = DBHelper()
    crawl(db_helper)
    generate_reports(db_helper)


if __name__ == '__main__':
    main()
