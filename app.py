import os
import pymysql
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, request, render_template, redirect, url_for, flash, session
app = Flask(__name__)

# @app.route('/')
@app.route('/login/', methods=['GET','POST'])
def login():
    error=None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            flash("Successfully logged in")
            # response = make_response(redirect(url_for('welcome')))
            # response.set_cookie('username', request.form.get('username'))
            # return response
            session['username'] = request.form.get('username')
            return redirect(url_for('welcome'))
        else:
            error = 'Incorrect'
            app.logger.warning("Incorrect username and password for user (%s)", request.form.get('username'))
    return render_template('login.html', error=error)

def valid_login(username, password):
    # mysql
    MYSQL_DATABASE_HOST = os.getenv('IP', '0.0.0.0')
    MYSQL_DATABASE_USER = 'fadziljusri'
    MYSQL_DATABASE_PASSWORD = ''
    MYSQL_DATABASE_DB = 'flask_app'
    conn = pymysql.connect(
        host=MYSQL_DATABASE_HOST,
        user=MYSQL_DATABASE_USER,
        passwd=MYSQL_DATABASE_PASSWORD,
        db=MYSQL_DATABASE_DB
        )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username='%s' AND password='%s'" % (username, password))
    data = cursor.fetchone()
    if data:
        return True
    else:
        return False
        
@app.route('/logout/')
def logout():
    # response = make_response(redirect(url_for('login')))
    # response.set_cookie('username', '', expires=0)
    # return response
    session.pop('username')
    return redirect(url_for('login'))
    
@app.route('/')
def welcome():
    # username = request.cookies.get('username')
    # if username:
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    return redirect(url_for('login'))
    
if __name__ == '__main__':
    host = os.getenv('IP','0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.debug = True
    app.secret_key = '\xe6\x8eV\xbaS\xbf\xe4\x0cM\x17\xe0\xa1{\xd6L\x94\xa8\x95\x19WIP\xb9O'
    
    # logging
    handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    
    app.run(host=host, port=port)