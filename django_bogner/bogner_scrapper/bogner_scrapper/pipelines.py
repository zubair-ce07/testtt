from products.models import Product, Category, Sku, Image


class BognerScrapperPipeline(object):
    def process_item(self, item, spider):
        try:
            product = Product.objects.get(retailer_sku=item['retailer_sku'])
            return item
        except(KeyError, Product.DoesNotExist):
            self.add_categories(item)
            item['description'] = self.convert_list_to_text(item['description'])
            item['care'] = self.convert_list_to_text(item['care'])
            product = Product(url=item['url'], retailer_sku=item['retailer_sku'], brand=item['brand'],
                              gender=item['gender'], name=item['name'], description=item['description'],
                              care=item['care'], market=item['market'], retailer=item['retailer'],
                              price=item['price'], currency=item['currency'], image_url=item['image_urls'][0])
            product.save()
            for cat in item['category']:
                category = Category.objects.get(category_name=cat)
                product.category.add(category)

            self.add_skus(item, product)
            self.add_images(item, product)
            return item

    def add_categories(self, item):
        for cat in item['category']:
            try:
                category = Category.objects.get(category_name=cat)
            except(KeyError, Category.DoesNotExist):
                category = Category(category_name=cat, image_url=item['image_urls'][0])
                category.save()

    def add_skus(self, item, product):
        for sku in item['skus']:
            new_sku = Sku(sku_id=sku['sku_id'], price=sku['price'], currency=sku['currency'], size=sku['size'],
                          color=sku['colour'], product=product)
            if sku.get('out-of-stock'):
                new_sku.out_of_stock = True
            new_sku.save()

    def add_images(self, item, product):
        for image_url in item['image_urls']:
            new_image = Image(image_url=image_url, product=product)
            new_image.save()

    def convert_list_to_text(self, mylist):
        text = ''
        for l in mylist:
            text += f"{l}. "
        return text
