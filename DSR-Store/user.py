from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from sqlalchemy import and_
from werkzeug.utils import secure_filename

from .models import Item, User, Order, Cart
from .models import db

user = Blueprint('user', __name__)

@user.route('/user_page')
@login_required
def user_page():
    """User will come to this page after log in and he will see all Item of Store"""
    data = []
    items = Item.query.all()
    
    for item in items:
        data.append(Item.row2json(Item, item))

    return render_template('user_page.html', items = data)

@user.route('/add_to_cart', methods = ['GET', 'POST'])
@login_required
def add_to_cart():
    """Add selected item  to the cart"""
    item_id = request.form['itemid']
    quantity = request.form['quantity']
    
    try:
        if check_inventory(quantity, item_id):
            if session.get('order_generated'):
                order_id = session['order_id']
               
                new_cart = Cart(item_id=item_id, quantity=quantity, order_id=order_id)
                db.session.add(new_cart)
                db.session.commit()
                flash(f"New item added to Cart")
               
            else:
                generate_order_id()
                order_id = session['order_id']
                # Insert into cart
                new_cart = Cart(item_id=item_id, quantity=quantity, order_id=order_id)
                db.session.add(new_cart)
                db.session.commit()
                flash(f"New item added to Cart")
                
        else:
            session.pop('_flashes', None)
            flash(f'The items you selected is Out of inventory')     
            return redirect(url_for('user.user_page'))
    except:
        session.pop('order_generated', None)
        session.pop('order_id', None)
        return redirect(url_for('user.user_page'))

    return redirect(url_for('user.show_cart'))

@user.route('/show_cart', methods = ['GET'])
@login_required
def show_cart():
    """Show Items that has been added to cart"""
    
    order_id = session['order_id']
    
    data = db.session.query(Cart.id, Cart.quantity, Item.name, Item.price).filter\
                     (and_(Item.id == Cart.item_id, Cart.order_id == order_id)).all()                  
    total = 0
    for items in data:
        total = total + items[3] * items[1]
    
    return render_template("cart.html", items = data, total = total)

@user.route('/remove_item/<string:id_data>', methods = ['GET'])
@login_required
def remove_item(id_data):
    """Remove items from cart"""
    try:
        cart = Cart.query.filter_by(id=id_data).first()
        db.session.delete(cart)
        db.session.commit()
        flash(f"items removed from cart")
    except:
        flash(f"Something is wrong! items could not be removed")

    return redirect(url_for('user.show_cart'))

@user.route('/clear_cart', methods = ['GET'])
@login_required
def clear_cart():
    """Discard all items from cart order is cancelled"""
    
    try:
        order_id = session['order_id']
        db.session.query(Cart).filter(Cart.order_id==order_id).delete()
        db.session.commit()
        
        order = Order.query.filter_by(id=order_id).first()
        db.session.delete(order)
        db.session.commit()
        
        session.pop('order_generated', None)
        session.pop('order_id', None)
        flash(f"Your cart is empty now")
    except:
        flash(f"Something is wrong! Cart is not empty")
    
    
    return redirect(url_for('user.user_page'))

@user.route('/checkout', methods = ['GET'])
@login_required
def checkout():
    order_id = session['order_id']
    
    data = []
    carts = db.session.query(Cart.item_id, Cart.quantity).filter(Cart.order_id==order_id).all()
    
    try:
        for cart in carts:
            items = Item.query.filter_by(id=cart.item_id).first()
            item.inventory = item.inventory - cart.quantity
            db.session.commit()
        flash(f"Order is placed Successfuly!")
    except:
        flash(f"Something is wrong! Order could not be placed try again!")

    session.pop('order_generated', None)
    session.pop('order_id', None)
    return redirect(url_for('user.user_page'))  

@user.route('/cur_user_orders', methods=['GET'])
@login_required
def cur_user_orders():
    """Shows orders of user that are pending"""
    user_id = session['userid']
    customers_data = db.session.query(Order.id, Order.status, User.name, User.address).filter\
                     (and_(Order.status == "Pending", Order.user_id == User.id, User.id == user_id)).all()

    return render_template('cur_user_orders.html', customers_data=customers_data) 

@user.route('/my_orders', methods=['GET'])
@login_required
def my_orders():
    """Shows previous orders"""
    user_id = session['userid']
    customers_data = db.session.query(Order.id, Order.status, User.name, User.address).filter\
                     (and_(Order.status == "Recieved", Order.user_id == user_id, User.id == user_id)).all()

    return render_template('cur_user_orders.html', customers_data=customers_data)     

@user.route('/order_recieved/<string:id_data>', methods=['GET'])
@login_required
def order_recieved(id_data):
    """Updates status of order if recieved by user"""

    try:
        order = Order.query.filter_by(id=id_data).first()
        order.status = "Recieved"
        db.session.commit()
        flash(f"Order is Recieved")
    except:
        flash(f"Something is wrong! Order status could not changed")
    
    return redirect(url_for('user.user_page'))           

def generate_order_id():
    user_id = session['userid']
    
    # Initialize order table
    try:
        new_order = Order(user_id=user_id)
        db.session.add(new_order)
        db.session.commit()
        flash(f"Order id generated")
    except:
        flash(f"Something is wrong! Order could not be generated")
    
    order = Order.query.filter_by(user_id=user_id).order_by(Order.id.desc()).first()
    order_id = order.id

    session['order_generated'] = True
    session['order_id'] = order_id    

def check_inventory(quantity, item_id):
    """checks if quantity of an item is available or not"""
    items = Item.query.filter_by(id=item_id).first()
    inventory = items.inventory
    return int(quantity) <= inventory
