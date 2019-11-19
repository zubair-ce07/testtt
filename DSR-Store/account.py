from flask import render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL,MySQLdb

from config import app
from main import main_page 
from user_main import user_main

mysql = MySQL(app)

@app.route('/', methods = ['POST','GET'])
def signup():
    session.pop('_flashes', None)
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']
        key = request.form['key']
        if key == "On":
            flash(f"Data Inserted Successfully")
            address = request.form['address']
            cur = mysql.connection.cursor()
            cur.execute(f"INSERT INTO accounts (name, password, address) VALUES (%s, %s, %s)", (name, password, address))
            mysql.connection.commit()
            return redirect(url_for('main_page'))
        else:
            return redirect(url_for('login',name = name, password = password))        
   
    return render_template('register.html')

@app.route('/login/<name>/<password>', methods = ['GET'])
def login(name, password):
    session.pop('_flashes', None)
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT password,user_id FROM accounts WHERE name = %s", (name,))
    user = cur.fetchone()
    cur.close
    try:
        if len(user) > 0:
            if name == "Admin" and password == "admin":
                flash(f"Admin logged in Succesfully")
                session['logged_in'] = True
                return redirect(url_for('main_page'))
            else:        
                if user[0] == password:
                    flash("logged in Succesfully")
                    session['logged_in'] = True
                    session['userid'] = user[1]
                    return redirect(url_for('user_main'))
                else:
                    return redirect(url_for('signup'))  
        else:
            return redirect(url_for('signup'))      
    except TypeError:
            return redirect(url_for('signup'))   
    
@app.route('/log_out', methods = ['POST','GET'])
def log_out():
    session.pop('_flashes', None)
    session.pop('logged_in', None)

   
    return render_template('register.html')

     
if __name__ == "__main__":
    app.run(debug=True)