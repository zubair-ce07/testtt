import json

from woolrich.models import *
from woolrich.constants import *


if __name__ == '__main__':
    db.create_all()

    with open('../woolrich.json') as input_file:
        products = json.load(input_file)
        categories = []

        for product in products:

            print('Loading Product with ID: {}'.format(product[PRODUCT_ID]))
            product_record = Product(
                _id=product.get(PRODUCT_ID), name=product.get(NAME), url=product.get(URL),
                img_url=product.get(IMG_URL), style_number=product.get(STYLE_NUMBER),
                brand=product.get(BRAND), description=product.get(DESCRIPTION)
            )

            db.session.add(product_record)
            db.session.commit()

            for category in product.get(CATEGORIES):

                if category in categories:
                    category_record = Category.query.filter(Category.name == category).first()
                else:
                    categories.append(category)
                    category_record = Category(name=category)
                    db.session.add(category_record)
                    db.session.commit()

                category_record.products.append(product_record)

            for feature in product.get(FEATURES):
                feature_record = Feature(description=feature, product=product_record)
                db.session.add(feature_record)

            for sku in product[SKUS]:

                sku_record = Sku(
                    sku_id=sku.get(SKU_ID), fit=sku.get(FIT),
                    color=sku.get(COLOR), size=sku.get(SIZE),
                    price=sku.get(PRICE), product=product_record,
                 )

                db.session.add(sku_record)
            db.session.commit()
