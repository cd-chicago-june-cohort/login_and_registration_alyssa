from flask import Flask, render_template, request, redirect, flash, session
from mysqlconnection import MySQLConnector
import re
import md5

app = Flask(__name__)
app.secret_key = "ShhhDontTell"
mysql = MySQLConnector(app, 'l_and_r')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = md5.new(request.form['password']).hexdigest()
    data = {'username': username, 'password': password}
    errors=True
    newUser=True
    query = 'select * from users where username = :username'
    db_check = mysql.query_db(query, data)
    # Check to see if user is already in database
    if len(db_check) == 1:
        newUser = False
    # Validations and error messages
    if len(username) < 1 or len(request.form['password']) < 1:
        flash("All fields are required!")
    elif not newUser and db_check[0]['password'] != password:
        flash('Incorrect password, please try again')
    else:
        errors=False
    # if not in database AND no errors, update database and go to success page
    
    if errors:
        return redirect('/')
    else:
        session['username'] = username
        if newUser:
            update = 'insert into users (username, password, created_at) values(:username, :password, NOW())'
            mysql.query_db(update, data)
            flash("You have successfully registered an account!  Welcome!")
        else: 
            flash("You have successfully logged in!  Welcome!")
            session['username'] = username
        return redirect ('/success')

@app.route('/success')
def success():
    return render_template('success.html')

    
app.run(debug=True)