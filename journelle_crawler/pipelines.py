from sqlalchemy.orm import sessionmaker
from journelle_crawler.models import Product, ImageURLS, SKUS, db_connect, create_table


class JournelleCrawlerPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()

        product = Product()
        product.retailer_sku = item['retailer_sku']
        product.gender = item['gender']
        product.category = item['category']
        product.brand = item['brand']
        product.url = item['url']
        product.date = item['date']
        product.currency = item['currency']
        product.market = item['market']
        product.retailer = item['retailer']
        product.url_original = item['url_original']
        product.name = item['name']
        product.description = ' '.join(item['description'])
        product.care = ' '.join(item['care'])
        product.price = item['price']
        product.spider_name = item['spider_name']
        product.crawl_start_time = item['crawl_start_time']

        image_urls = ImageURLS()
        image_urls.retailer_sku = item['retailer_sku']
        image_urls.image_urls = ', '.join(item['image_urls'])

        try:
            session.add(product)
            session.add(image_urls)

            for sku_id, sku in item['skus'].items():
                sku_item = SKUS()
                sku_item.retailer_sku = item['retailer_sku']
                sku_item.sku_id = sku_id
                sku_item.price = sku['price']
                sku_item.currency = sku['currency']
                sku_item.size = sku['size']
                sku_item.out_of_stock = sku['out_of_stock']
                session.add(sku_item)

            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

        return item
