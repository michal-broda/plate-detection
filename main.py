from flask import Flask, render_template, current_app
from flask_login import current_user
import flask_login
import flask
import login
import sqlalchemy as db
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker


#import mysql.connector
#import os
#import html


app = Flask(__name__)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
app.secret_key = 'string'

users = {'michal': {'password': 'secret'}}
stringinpage = "michl"

engine = create_engine('sqlite:///plate.sqlite')
session = sessionmaker(engine)
connection = engine.connect()
metadata = MetaData()




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



plate = [{
    "id": 1,
    "date": "11.22.2023",
    "hour": "19:23",
    "plate": "KR 21212",
    "image": "static/d.jpg"
},
    {
        "id": 2,
        "date": "22.22.2023",
        "hour": "09:23",
        "plate": "rja 21212",
        "image": "5.jpg"
    },
    {
        "id": 3,
        "date": "22.22.2023",
        "hour": "09:23",
        "plate": "rsds21212",
        "image": "5.jpg"
    },
    {
        "id": 4,
        "date": "22.22.2023",
        "hour": "09:23",
        "plate": "ds212",
        "image": "5.jpg"
    },
    {
        "id": 5,
        "date": "22.22.2023",
        "hour": "09:23",
        "plate": "ds212",
        "image": "5.jpg"
    }

]


##########################
length = len(plate)
table = ""

for j in range(length):
    temp = list(plate[j].values())
    table += "<tr>"
    for i in temp:
        table += "<td>" + str(i) + "</td>"
    table += "</tr>"
#print(table)
#trzeba użyć   {{string|safe}}



@app.route('/')
def home_page():
    return render_template('index.html', PLATE=plate, LOG=login_bar(), string=stringinpage, TAB=table,
                           LOGOUT=login_bar_logout())


if __name__ == '__main__':
    app.run(debug=True)

