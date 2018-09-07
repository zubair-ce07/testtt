import json

from flask import Blueprint, render_template, url_for, request, Response
from sqlalchemy import or_
from sqlalchemy.ext.declarative import DeclarativeMeta
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from .auth import login_required
from .database import db_session
from .models import Item

bp = Blueprint('item', __name__)


@bp.route('/')
def index():
    items = db_session.query(Item).order_by(Item.id).all()
    return render_template('item/index.html', items=items)


@bp.route('/load', methods=('GET', 'POST'))
@login_required
def load():
    return render_template('item/load.html')


@bp.route("/load_items/", methods=['POST'])
def move_forward():
    db_session.query(Item).delete()
    db_session.commit()
    from . import my_crawler
    my_crawler.schedule()
    return redirect(url_for('index'))


@bp.route("/<int:item_id>/jsondata", methods=['GET', 'POST'])
def view_json(item_id):
    item = db_session.query(Item).filter(Item.identifier == item_id).first()
    json_item = json.dumps(item, cls=AlchemyEncoder, sort_keys=True, indent=4)
    resp = Response(json_item)
    resp.headers['Content-Type'] = 'application/json'
    return resp


@bp.route('/product', methods=['POST'])
def view_product_listing():
    search = request.form['search']
    search_result = db_session.query(Item).filter(or_(Item.brand.like(search),
                                                      Item.identifier.like(search),
                                                      Item.product_name.like(search))).all()
    return render_template('item/product_listing.html',
                           items=search_result)


@bp.route('/<int:item_id>/viewProd', methods=['GET', 'POST'])
def view_product(item_id):
    item = db_session.query(Item).filter(Item.identifier == item_id).first()
    return render_template('item/view_product.html',
                           item=item)


def get_post(item_sku):
    post = db_session.query(Item).filter(Item.retailer_sku == item_sku).first()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(item_sku))

    return post


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    pass
            # a json-encodable dict
            return fields
        return json.JSONEncoder.default(self, obj)
