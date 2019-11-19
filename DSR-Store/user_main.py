from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_mysqldb import MySQL, MySQLdb
from datetime import datetime

app = Flask(__name__)
from config import app, database
mysql = MySQL(app)



@app.route('/user_main', methods=['GET', 'POST'])
def user_main():
    """User will come to this page after log in and he will see all Items of Store"""
    if session.get('logged_in'):
        cursor = database.cursor()
        query_string = f"SELECT * FROM items"
        cursor.execute(query_string)
        data = cursor.fetchall()
        return render_template('user_main.html', items = data)
    else:
        return redirect(url_for('signup'))    
   

@app.route('/addcart', methods = ['GET', 'POST'])
def add_to_cart():
    """Add selected Item  to the cart"""
    item_id = request.form['itemid']
    quantity = request.form['quantity']
    cur_date = datetime.now().date() 
    
    if check_inventory(quantity, item_id):
        if session.get('order_generated'):
            order_id = session['order_id']
            cur = database.cursor()
            query_string = f"INSERT INTO carts (item_id,quantity, order_id) VALUES ({item_id},{quantity},{order_id})"
            cur.execute(query_string)
            database.commit()
        else:
            generate_order_id()
            order_id = session['order_id']
            cur = database.cursor()
            query_string = f"INSERT INTO carts (item_id,quantity, order_id) VALUES ({item_id},{quantity},{order_id})"
            cur.execute(query_string)
            database.commit()
    else:
        session.pop('_flashes', None)
        flash(f'The item you selected is Out of inventory')     
        return redirect(url_for('user_main')) 

    return redirect(url_for('show_cart'))

@app.route('/show_cart', methods = ['GET'])
def show_cart():
    """Show Items that has been added to cart"""
    order_id = session['order_id']
    cursor = database.cursor()
    query_string = f"""SELECT carts.cart_id, carts.quantity, items.name, items.price
                      FROM items
                      RIGHT JOIN carts
                      ON items.item_id=carts.item_id WHERE carts.order_id={order_id}"""
    cursor.execute(query_string)
    data = cursor.fetchall()
    total = 0
    for item in data:
        total = total + item[3] * item[1]
    
    return render_template("cart.html", items = data, total = total)

@app.route('/remove_item/<string:id_data>', methods = ['GET'])
def remove_item(id_data):
    """Remove item from cart"""
    cur = database.cursor()
    cur.execute(f"DELETE FROM carts WHERE cart_id=%s", (id_data,))
    database.commit()
    return redirect(url_for('show_cart'))         

@app.route('/clear_cart', methods = ['GET'])
def clear_cart():
    """Discard all items from cart order is cancelled"""
    order_id = session['order_id']
    cur = database.cursor()
    cur.execute(f"DELETE FROM carts WHERE order_id=%s", (order_id,))
    database.commit()
    
    cur.execute(f"DELETE FROM orders WHERE order_id=%s", (order_id,))
    database.commit()

    session.pop('order_generated', None)
    session.pop('order_id', None)
    return redirect(url_for('user_main'))

@app.route('/checkout', methods = ['GET'])
def checkout():
    order_id = session['order_id']
    cursor = database.cursor()
    query_string = f"SELECT item_id, quantity FROM carts where order_id = {order_id};"
    cursor.execute(query_string)
    order = cursor.fetchall()
    
    """Update the inventory of items by substracting quantity"""
    for items in order:
        cursor = database.cursor()
        query_string = f"UPDATE items SET inventory = inventory-{items[1]} WHERE item_id = {items[0]}"
        cursor.execute(query_string)
        database.commit()
    

    session.pop('order_generated', None)
    session.pop('order_id', None)
    return redirect(url_for('user_main'))

@app.route('/cur_user_orders', methods=['GET'])
def cur_user_orders():
    """Shows orders of user that are pending"""
    user_id = session['userid']
    cursor = database.cursor()
    query_string = f"""SELECT orders.order_id, orders.status, accounts.name, accounts.address
                      FROM orders
                      INNER JOIN accounts
                      ON orders.user_id = accounts.user_id WHERE 
                      orders.status="Pending" and orders.user_id = {user_id}"""
    cursor.execute(query_string)
    customers_data = cursor.fetchall()
    return render_template('cur_user_orders.html', customers_data=customers_data) 

@app.route('/my_orders', methods=['GET'])
def my_orders():
    """Shows previous orders"""
    user_id = session['userid']
    cursor = database.cursor()
    query_string = f"""SELECT orders.order_id, orders.status, accounts.name, accounts.address
                      FROM orders
                      INNER JOIN accounts
                      ON orders.user_id = accounts.user_id WHERE 
                      orders.status="Recieved" and orders.user_id = {user_id}"""
    cursor.execute(query_string)
    customers_data = cursor.fetchall()
    return render_template('cur_user_orders.html', customers_data=customers_data)     

@app.route('/order_recieved/<string:id_data>', methods=['GET'])
def order_recieved(id_data):
    """Updates status of order if recieved by user"""
    cursor = database.cursor()
    query_string = f"UPDATE orders SET status = 'Recieved' WHERE order_id = {id_data}"
    cursor.execute(query_string)
    database.commit()
    return redirect(url_for('user_main'))                             

def generate_order_id():
    user_id = session['userid']
    cur_date = datetime.now().date()
    cur = database.cursor()
    query_string = f"INSERT INTO orders (user_id, on_date) VALUES ({user_id},'{cur_date}')"
    cur.execute(query_string)
    database.commit()

    cursor = database.cursor()
    query_string = f"SELECT max(order_id) FROM orders where user_id={user_id};"
    cursor.execute(query_string)
    order_id = cursor.fetchone()[0]

    session['order_generated'] = True
    session['order_id'] = order_id

def check_inventory(quantity, item_id):
    """checks if quantity of an item is available or not"""
    cursor = database.cursor()
    query_string = f"SELECT inventory FROM items where item_id={item_id};"
    cursor.execute(query_string)
    inventory = cursor.fetchone()[0]
    return True if int(quantity) <= inventory else False
     
    
