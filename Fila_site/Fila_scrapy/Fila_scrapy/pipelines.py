

from Fila.models import Product, Skus

class FilaScrapyPipeline(object):

    def process_item(self, item, spider):

        product = Product(Retailer_Sku = item['retailer_sku'], Gender = item['gender'], Brand = item['brand'],
                        Url = item['url'], Name = item['name'], Description = item['description'],
                        Care = item['care'],  Image_url = ' '.join(map(str, item['image_urls'])) 
        )

        product.save()
        
        if item['skus']:
            for sku_id, sku_dic in item['skus'].items():                

                sku = Skus(Retailer_Sku = product, Sku_id = sku_dic['sku_id'], Size = sku_dic['size'],
                        Color = sku_dic['color'], Currency = sku_dic['currency'], Price = sku_dic['price']
                )

                sku.save()

        return item
