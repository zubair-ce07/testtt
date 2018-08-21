from woolrich import db, ma


Product_Category = db.Table(
    'product_category',
    db.Column('product_id', db.Integer, db.ForeignKey('product._id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category._id'))
)


class Product(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(256), nullable=False)
    img_url = db.Column(db.String(256))
    style_number = db.Column(db.String(16), nullable=False)
    brand = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(1024))
    features = db.relationship('Feature', backref='product')
    skus = db.relationship('Sku', backref='product')
    categories = db.relationship('Category', secondary=Product_Category,
                                 backref=db.backref('products', lazy='dynamic'))

    def __iter__(self):
        return self.to_dict().iteritems()

    def __repr__(self):
        return '<Product _id: {}>'.format(self._id)


class Feature(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product._id'))

    def __repr__(self):
        return '<Feature _id: {}>'.format(self.description)

    def __iter__(self):
        return self.to_dict().iteritems()


class Category(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<Category _id: {}>'.format(self.name)

    def __iter__(self):
        return self.to_dict().iteritems()


class Sku(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    sku_id = db.Column(db.String(16), nullable=False)
    fit = db.Column(db.String(16))
    price = db.Column(db.String(16), nullable=False)
    color = db.Column(db.String(64), nullable=False)
    size = db.Column(db.String(128), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product._id'))

    def __iter__(self):
        return self.to_dict().iteritems()

    def __repr__(self):
        return '<Sku sku_id: {}>'.format(self.sku_id)


class CategorySchema(ma.ModelSchema):
    class Meta:
        model = Category


class SkuSchema(ma.ModelSchema):
    class Meta:
        model = Sku


class FeatureSchema(ma.ModelSchema):
    class Meta:
        model = Feature


class ProductSchema(ma.ModelSchema):
    categories = ma.Nested(CategorySchema, only='name', many=True)
    features = ma.Nested(FeatureSchema, only='description', many=True)
    skus = ma.Nested(SkuSchema, only=('sku_id', 'price', 'color', 'size'), many=True)

    class Meta:
        model = Product
