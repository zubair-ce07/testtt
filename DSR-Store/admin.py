from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from werkzeug.utils import secure_filename
import os
from sqlalchemy import and_

from .models import Item, User, Order, Cart, session
from . import db

app = Flask(__name__)
UPLOAD_FOLDER = f'/home/ashfaq/Desktop/weatherman/DSR-Store/static/image_holder'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

admin = Blueprint('admin', __name__)

@admin.route('/page', methods = ['GET'])
@login_required
def page():
    data = []
    item = Item.query.all()
    
    for item in item:
        data.append(Item.row2json(Item, item))
    
    return render_template('admin_page.html', item = data)

@admin.route('/insert', methods = ['POST'])
def insert():
    """Insers new Item"""
    if request.method == "POST":
        flash(f"Data Inserted Successfully")
        name = request.form['name']
        price = request.form['price']
        unit = request.form['unit']
        inventory = request.form['inventory']
        image_path = f"image_holder/image.png"
        
        # create new user and add to database
        new_item = Item(name=name, price=price, unit=unit, inventory=inventory, image_path=image_path)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('admin.page'))

@admin.route('/update',methods=['POST','GET'])
def update():
    """Update detail of Item"""
    if request.method == 'POST':
        item_id = request.form['id']
        name = request.form['name']
        price = request.form['price']
        unit = request.form['unit']
        inventory = request.form['inventory']
        
        item = Item.query.filter_by(id=item_id).first()
        item.name, item.price, item.unit, item.inventory = name, price, unit, inventory
        db.session.flush()
        db.session.commit()
        return redirect(url_for('admin.page'))

@admin.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    item = Item.query.filter_by(id=id_data).first()
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('admin.page'))

@admin.route('/upload_image/<string:id_data>', methods = ['POST','GET'])
def upload_image(id_data):
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
            image_path = f'image_holder/{filename}' 
            
            item = Item.query.filter_by(id=id_data).first()
            item.image_path = image_path
            db.session.flush()
            db.session.commit()

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('admin.page'))
    
    #get image from database to display
    item = Item.query.filter_by(id=id_data).first()
    image_path = item.image_path
    
    return render_template('upload_image.html', user_image=image_path)

def allowed_file(filename):
    """check if extension is allowed for image upload"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin.route('/cur_orders', methods=['GET'])
def cur_orders():
    """Show Orders that are in process"""
    customers_data = db.session.query(Order.id, Order.status, User.name, User.address).filter\
                     (and_(Order.status == "Pending", Order.user_id == User.id)).all()
    
    return render_template('cur_orders.html', customers_data=customers_data)

@admin.route('/orders_history', methods=['GET'])
def orders_history():
    """Show previous Orders that has been delivered"""
    customers_data = db.session.query(Order.id, Order.status, User.name, User.address).filter\
                     (and_(Order.status == "Recieved", Order.user_id == User.id)).all()

    return render_template('cur_orders.html', customers_data=customers_data)         

@admin.route('/order_detail/<string:id_data>', methods=['GET'])
def order_detail(id_data):
    data = db.session.query(Cart.id, Cart.quantity, Item.name, Item.price).filter\
                     (and_(Item.id == Cart.item_id, Cart.order_id == id_data)).all()                  
    total = 0
    for item in data:
        total = total + item[3] * item[1]
    
    return render_template("order_detail.html", items = data, total = total)        