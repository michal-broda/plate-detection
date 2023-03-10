import sqlite3
from datetime import date

from flask import Flask, render_template, current_app
from flask_login import current_user
import flask_login
import flask
from sqlalchemy import create_engine, MetaData, select, text
from sqlalchemy.orm import sessionmaker

from dbi import create_connection, create_users, drop_users

#import mysql.connector
#import os
#import html

plate_first = (
    "michal",
    "sasadsa",
    "sads@sas.pl",
    False,
)

app = Flask(__name__)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
app.secret_key = 'string'

users = {'michal': {'password': 'secret'}}
stringinpage = "michgl"
sql_url = "sqlite:///data.db"
engine = create_engine(sql_url)
session = sessionmaker(engine)
connection = engine.connect()
metadata = MetaData()



#create_connection(r"plate.sqlite")
conn = sqlite3.connect("data.db")


#create_users(conn, plate_first)
#drop_users(conn, connection)
#if conn:
#    conn.close()


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user




@app.route('/login', methods=['GET', 'POST'])
def login():
############
    print(current_user.is_authenticated)
    print(current_app.login_manager.unauthorized())
############
    if flask.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit' class='btn btn-secondary btn-sm' style='margin-top:-5px';/>
               </form>
               '''

    email = flask.request.form['email']
    if email in users and flask.request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))

    return 'Bad login'

def login_bar():
    if current_user.is_authenticated == False:
        return login()
    else:
        return 'Logged in as: ' + flask_login.current_user.id

def login_bar_logout():
    if current_user.is_authenticated == False:
        return ''
    else:
        return '''<a type="button" href="/logout" class="btn btn-secondary btn-sm"; style="margin-top:-6px; ' 
               --bs-btn-font-size: .75rem;">Log out</a>'''


@app.route('/protected')
@flask_login.login_required
def protected():
    return render_template('protected.html', LOG=login_bar(), LOGOUT=login_bar_logout(), USER=flask_login.current_user.id)


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return render_template('logout.html', LOG=login_bar())


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401


xx = drop_users(conn, connection)

@app.route('/')
def home_page():
    return render_template('index.html', PLATE=xx, LOG=login_bar(), string=stringinpage,
                           LOGOUT=login_bar_logout())


if __name__ == '__main__':
    print("--------------")

    app.run(debug=True)


#drop_users(conn, connection)
if conn:
    conn.close()