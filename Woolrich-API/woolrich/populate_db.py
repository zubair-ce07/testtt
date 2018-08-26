import json

from woolrich.models import *
from woolrich.constants import Constants


if __name__ == '__main__':
    db.create_all()

    with open('woolrich.json') as input_file:
        products = json.load(input_file)
        categories = []

        for product in products:

            print('Loading Product with ID: {}'.format(product[Constants.PRODUCT_ID]))
            product_record = Product(
                _id=product[Constants.PRODUCT_ID], name=product[Constants.NAME], url=product[Constants.URL],
                img_url=product[Constants.IMG_URL], style_number=product[Constants.STYLE_NUMBER],
                brand=product[Constants.BRAND], description=product[Constants.DESCRIPTION]
            )

            db.session.add(product_record)
            db.session.commit()

            for category in product[Constants.CATEGORIES]:

                category_record = None

                if category in categories:
                    category_record = Category.query.filter(Category.name == category).first()
                else:
                    categories.append(category)
                    category_record = Category(name=category)
                    db.session.add(category_record)
                    db.session.commit()

                category_record.products.append(product_record)

            for feature in product[Constants.FEATURES]:
                feature_record = Feature(description=feature, product=product_record)
                db.session.add(feature_record)

            for sku in product[Constants.SKUS]:

                if not sku.get(Constants.SIZE):
                    sku[Constants.SIZE] = None

                if not sku.get(Constants.FIT):
                    sku[Constants.FIT] = None

                sku_record = Sku(
                    sku_id=sku[Constants.SKU_ID], fit=sku[Constants.FIT],
                    color=sku[Constants.COLOR], size=sku[Constants.SIZE],
                    price=sku[Constants.PRICE], product=product_record,
                 )

                db.session.add(sku_record)
            db.session.commit()
