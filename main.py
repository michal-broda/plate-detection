import sqlite3
from datetime import date

from flask import Flask, render_template, current_app
from flask_login import current_user
import flask_login
import flask
from sqlalchemy import create_engine, MetaData, select, text
from sqlalchemy.orm import sessionmaker

from dbi import create_connection, create_users, get_plate, create_plates

"""
    plate_first = (
    "11.02.1999",
    "1 1:12",
    "WW 1234",
    False,
    )
"""

app = Flask(__name__)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
app.secret_key = 'string'

users = {'michal': {'password': 'secret'}}
stringinpage = "michl"
sql_url = "sqlite:///data.db"
engine = create_engine(sql_url)
session = sessionmaker(engine)
connection = engine.connect()
metadata = MetaData()

# create_connection(r"plate.sqlite")
conn = sqlite3.connect("data.db")

"""
    for i in range(10): create_plates(conn, plate_first)
    if conn:
    conn.close()
"""


class User(flask_login.UserMixin):
    pass


class Quest():
    """ form in search page """
    def __init__(self, data, hour, plate):
        self.data = data
        self.hour = hour
        self.plate = plate

    def show(self):
        print(f'data: {self.data}')
        print(f'hour: {self.hour}')
        print(f'plate: {self.plate}')


""" all action flask """
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
    print(current_user.is_authenticated)
    print(current_app.login_manager.unauthorized())

    if flask.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit' class='btn btn-secondary btn-sm' style='margin-top:-5px';/>
               </form>
               '''

    email = flask.request.form['email']

    # print(email)
    # print(flask.request.form['password'])

    if email in users and flask.request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))

    return 'Bad login'


def login_bar():
    if not current_user.is_authenticated:
        return login()
    else:
        return 'Logged in as: ' + flask_login.current_user.id


def login_bar_logout():
    if not current_user.is_authenticated:
        return ''
    else:
        return '''<a type="button" href="/logout" class="btn btn-secondary btn-sm"; style="margin-top:-6px; ' 
               --bs-btn-font-size: .75rem;">Log out</a>'''


@app.route('/protected')
@flask_login.login_required
def protected():
    return render_template('protected.html', LOG=login_bar(), LOGOUT=login_bar_logout(),
                           USER=flask_login.current_user.id)


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return render_template('logout.html', LOG=login_bar())


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401


@app.route('/search', methods=['GET', 'POST'])
def search():
    if flask.request.method == 'GET':
        return '''
                <form action='search' method='POST'>
                <input type='text' name='day' id='day' placeholder='day'/>
                <input type='text' name='hour' id='hour' placeholder='hour'/>
                <input type='text' name='plate' id='hour' placeholder='plate'/>
                <input type='submit' name='search' class='btn btn-secondary btn-sm' style='margin-top:-5px';/>
               </form>
               '''
    request = Quest(flask.request.form['day'], flask.request.form['hour'], flask.request.form['plate'])

    # print(request.hour, request.data, request.plate)

    """ connecting db """
    engine = create_engine(sql_url)
    session = sessionmaker(engine)
    connection = engine.connect()
    metadata = MetaData()
    conn = sqlite3.connect("data.db")
    ss = get_plate(conn, connection, search=True, data=request.data, hour=request.hour,
                   plate=request.plate)

    return render_template('search_page.html', PLATE=ss)


xx = get_plate(conn, connection)


@app.route('/')
def home_page():
    return render_template('index.html', PLATE=xx, LOG=login_bar(), string=stringinpage,
                           LOGOUT=login_bar_logout(), SEARCH=search())


@app.route('/search_page')
def search_page():
    return render_template('search_page.html', PLATE=xx,
                           LOG=login_bar(), string=stringinpage,
                           LOGOUT=login_bar_logout(), SEARCH=search())


if __name__ == '__main__':
    print("--------------")

    app.run(debug=True, port=5095)


if conn:
    conn.close()
