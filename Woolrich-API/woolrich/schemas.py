from woolrich import marshmallow_app
from woolrich.models import Category, Feature, Sku, Product


class CategorySchema(marshmallow_app.ModelSchema):
    class Meta:
        model = Category


class SkuSchema(marshmallow_app.ModelSchema):
    class Meta:
        model = Sku


class FeatureSchema(marshmallow_app.ModelSchema):
    class Meta:
        model = Feature


class ProductSchema(marshmallow_app.ModelSchema):
    categories = marshmallow_app.Nested(CategorySchema, only='name', many=True)
    features = marshmallow_app.Nested(FeatureSchema, only='description', many=True)
    skus = marshmallow_app.Nested(SkuSchema, only=('sku_id', 'price', 'color', 'size'), many=True)

    class Meta:
        model = Product
