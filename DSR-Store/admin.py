import os

from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required
from werkzeug.utils import secure_filename
from sqlalchemy import and_

from . import db
from .models import Item, User, Order, Cart

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/image_holder/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

admin = Blueprint('admin', __name__)

@admin.route('/admin_page', methods = ['GET'])
@login_required
def admin_page():
    data = []
    items = Item.query.all()
    
    for item in items:
        data.append(Item.row2json(Item, item))
    
    return render_template('admin_page.html', items = data)

@admin.route('/insert_item', methods = ['POST'])
@login_required
def insert_item():
    """Insert new Item"""
    if request.method == "POST":
        flash(f"Data Inserted Successfully")
        name = request.form['name']
        price = request.form['price']
        unit = request.form['unit']
        inventory = request.form['inventory']
        image_path = f"image_holder/image.png"
        
        # Insert new Item
        try:
            new_items = Item(name=name, price=price, unit=unit, inventory=inventory, image_path=image_path)
            db.session.add(new_item)
            db.session.commit()
            flash(f"{name} inserted Successfully")
        except:
            flash(f"Something is wrong! data could not insert")
        
        return redirect(url_for('admin.page'))

@admin.route('/update_item',methods=['POST','GET'])
@login_required
def update_item():
    """Update detail of Item"""
    session.pop('_flashes', None)
    if request.method == 'POST':
        item_id = request.form['id']
        name = request.form['name']
        price = request.form['price']
        unit = request.form['unit']
        inventory = request.form['inventory']
        
        try:
            items = Item.query.filter_by(id=item_id).first()
            items.name, items.price, items.unit, items.inventory = name, price, unit, inventory
            db.session.commit()
            flash(f"{name} Updated Successfully")
        except:
            flash(f"Something is wrong! data could not update")

        return redirect(url_for('admin.admin_page'))
        
@admin.route('/delete_item/<string:id_data>', methods = ['GET'])
@login_required
def delete_item(id_data):
    try:
        items = Item.query.filter_by(id=id_data).first()
        db.session.delete(items)
        db.session.commit()
        flash(f"items deleted Successfully")
    except:
        flash(f"Something is wrong! data could not deleted")
    
    return redirect(url_for('admin.admin_page'))

@admin.route('/upload_image', methods = ['POST','GET'])
@login_required
def upload_image():
    """Uploads image of Item"""
    if request.method == 'POST':
        id_data = request.form['id']
        # check if the post request has the file part
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        image = request.files['image']
        
        # if user does not select file, browser also
        # submit an empty part without filename
        if image.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
             
        try:
            # Store file path in Mysql
            image_path = f'image_holder/{filename}' 
            items = Item.query.filter_by(id=id_data).first()
            items.image_path = image_path
            db.session.commit()
            flash(f"{items.name} Updated Successfully")  
        except:
            flash(f"Something is wrong! Image could not update")
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('admin.admin_page'))
               
def allowed_file(filename):
    """check if extension is allowed for image upload"""
    return '.' in filename and \
           filename.split('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin.route('/cur_orders', methods=['GET'])
@login_required
def cur_orders():
    """Show Orders that are in process"""
    customers_data = db.session.query(Order.id, Order.status, User.name, User.address).filter\
                     (and_(Order.status == "Pending", Order.user_id == User.id)).all()
    
    return render_template('cur_orders.html', customers_data=customers_data)

@admin.route('/orders_history', methods=['GET'])
@login_required
def orders_history():
    """Show previous Orders that has been delivered"""
    customers_data = db.session.query(Order.id, Order.status, User.name, User.address).filter\
                     (and_(Order.status == "Recieved", Order.user_id == User.id)).all()

    return render_template('cur_orders.html', customers_data=customers_data)         

@admin.route('/order_detail/<string:id_data>', methods=['GET'])
@login_required
def order_detail(id_data):
    data = db.session.query(Cart.id, Cart.quantity, Item.name, Item.price).filter\
                     (and_(Item.id == Cart.item_id, Cart.order_id == id_data)).all()                  
    total = 0
    for items in data:
        total = total + items[3] * items[1]
    
    return render_template("order_detail.html", items = data, total = total)

