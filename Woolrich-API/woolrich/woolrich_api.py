from flask import render_template, jsonify

from woolrich.models import *
from woolrich.schemas import ProductSchema
from woolrich import app


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/api/product/<product_id>')
def product_by_id(product_id):
    product_schema = ProductSchema()
    product = Product.query.filter_by(_id=int(product_id)).first()
    output_product = product_schema.dump(product).data

    return jsonify({'product': output_product})


@app.route('/api/products/<quantity>')
def products_by_quantity(quantity):
    product_schema = ProductSchema(many=True)
    products = Product.query.limit(int(quantity)).all()
    output_products = product_schema.dump(products).data

    return jsonify({'product': output_products})


if __name__ == '__main__':
    app.run(debug=True)
