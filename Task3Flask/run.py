from flask import Flask, render_template, request, url_for 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Product, Product_Variation, Product_Size

app = Flask(__name__)

engine = create_engine('sqlite:///ChildrensPlace.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/ChildrensPlace/')
def ChildrenPlace():
    product = session.query(Product).first()
    variation = session.query(Product_Variation).filter_by(store_keeping_unit=product.store_keeping_unit).all()
    sizes = session.query(Product_Size).filter_by(store_keeping_unit=product.store_keeping_unit).all()    
    return render_template('productdetail.html', product=product, variation=variation, sizes=sizes)



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

