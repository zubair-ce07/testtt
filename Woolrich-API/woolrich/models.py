from woolrich import db


ProductCategory = db.Table(
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
    categories = db.relationship('Category', secondary=ProductCategory,
                                 backref=db.backref('products', lazy='dynamic'))

    def __repr__(self):
        return '<Product _id: {}>'.format(self._id)


class Feature(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product._id'))

    def __repr__(self):
        return '<Feature description: {}>'.format(self.description)


class Category(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<Category name: {}>'.format(self.name)


class Sku(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    sku_id = db.Column(db.String(16))
    fit = db.Column(db.String(16))
    price = db.Column(db.String(16))
    color = db.Column(db.String(64))
    size = db.Column(db.String(128))
    product_id = db.Column(db.Integer, db.ForeignKey('product._id'))

    def __repr__(self):
        return '<Sku sku_id: {}>'.format(self.sku_id)
