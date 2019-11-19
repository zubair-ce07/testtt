from flask import render_template, request, redirect, url_for, flash,Flask, send_from_directory, session
from flask_mysqldb import MySQL

from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

from config import app, database

UPLOAD_FOLDER = f'/home/ashfaq/Environments/DSR-Store/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mysql = MySQL(app)

@app.route('/index', methods=['GET', 'POST'])
def main_page():
    """Admin will come to this page and this page will show items of his general store"""
    if session.get('logged_in'):
        cursor = database.cursor()
        query_string = f"SELECT * FROM items"
        cursor.execute(query_string)
        data = cursor.fetchall()
        
        return render_template('index.html', items = data)
    else:
        return redirect(url_for('signup'))    

@app.route('/insert', methods = ['POST'])
def insert():
    """Insers new Item"""
    if request.method == "POST":
        flash(f"Data Inserted Successfully")
        name = request.form['name']
        price = request.form['price']
        unit = request.form['unit']
        inventory = request.form['inventory']
        image_path = f"/uploads/image.png"
        
        cur = database.cursor()
        cur.execute(f"""INSERT INTO items (name, price, unit, inventory, image_path) 
        VALUES (%s, %s, %s, %s, %s)""", (name, price, unit, inventory, image_path))
        database.commit()
        return redirect(url_for('main_page'))    

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash(f"Record Has Been Deleted Successfully")
    cur = database.cursor()
    cur.execute(f"DELETE FROM items WHERE item_id=%s", (id_data,))
    database.commit()
    return redirect(url_for('main_page'))

def allowed_file(filename):
    """check if extension is allowed for image upload"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload/<string:id_data>', methods = ['POST','GET'])
def upload(id_data):
    """Uploads image of Item"""
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            #Store file path in Mysql
            image_path = f'/uploads/{filename}' 
            cur = database.cursor()
            cur.execute(f"UPDATE items SET image_path=%s WHERE item_id=%s", (image_path,id_data))
            database.commit()

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('main_page'))
    
    #get image from db to display
    cursor = database.cursor()
    query_string = f"SELECT image_path FROM items WHERE item_id="+id_data
    cursor.execute(query_string)
    data = cursor.fetchone()
    image_path = str =  ''.join(data)
    
    return render_template('upload.html', user_image=image_path)

@app.route('/update',methods=['POST','GET'])
def update():
    """Update detail of Item"""
    if request.method == 'POST':
        item_id = request.form['id']
        name = request.form['name']
        price = request.form['price']
        unit = request.form['unit']
        inventory = request.form['inventory']
        cur = database.cursor()
        cur.execute(f"""
               UPDATE items
               SET name=%s, price=%s, unit=%s, inventory=%s
               WHERE item_id=%s
            """, (name, price, unit, inventory, item_id))
        flash("Data Updated Successfully")
        database.commit()
        return redirect(url_for('main_page'))

@app.route('/cur_orders', methods=['GET'])
def cur_orders():
    """Show Orders that are in process"""
    cursor = database.cursor()
    query_string = f"""SELECT orders.order_id, orders.status, accounts.name, accounts.address
                      FROM orders
                      INNER JOIN accounts
                      ON orders.user_id = accounts.user_id WHERE orders.status="Pending" """
    cursor.execute(query_string)
    customers_data = cursor.fetchall()
    return render_template('cur_orders.html', customers_data=customers_data)

@app.route('/orders_history', methods=['GET'])
def orders_history():
    """Show previous Orders that has been delivered"""
    cursor = database.cursor()
    query_string = f"""SELECT orders.order_id, orders.status, accounts.name, accounts.address
                      FROM orders
                      INNER JOIN accounts
                      ON orders.user_id = accounts.user_id WHERE orders.status="Recieved" """
    cursor.execute(query_string)
    customers_data = cursor.fetchall()
    return render_template('cur_orders.html', customers_data=customers_data)    

@app.route('/order_detail/<string:id_data>', methods=['GET'])
def order_detail(id_data):
    """Show detail of selected order to see what he ordered and total bill"""
    cursor = database.cursor()
    query_string = f"""SELECT carts.cart_id, carts.quantity, items.name, items.price
                      FROM items
                      RIGHT JOIN carts
                      ON items.item_id=carts.item_id WHERE carts.order_id={id_data}"""
    cursor.execute(query_string)
    data = cursor.fetchall()
    total = 0
    for item in data:
        total = total + item[3] * item[1]
    return render_template("order_detail.html", items = data, total = total)    