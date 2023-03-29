import sqlite3
import string
from sqlite3 import Error

from sqlalchemy import select, text


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Version :", sqlite3.version)
    except Error as e:
        print(e)


def create_users(conn, data):
    cur = conn.cursor()
    sql = f''' INSERT INTO users(name,password,email,admin)
              VALUES(?,?,?,?) '''
    cur.execute(sql, data)
    # cur.execute("INSERT INTO users(name,password,email) VALUES ('rob','sasasas','sa@sa.sa')")
    conn.commit()
    return print(cur.lastrowid)  # how much values


def create_plates(conn, data):
    cur = conn.cursor()
    sql = f''' INSERT INTO plates(date,hour,plate,image)
              VALUES(?,?,?,?) '''
    cur.execute(sql, data)
    # cur.execute("INSERT INTO users(name,password,email) VALUES ('rob','sasasas','sa@sa.sa')")
    conn.commit()
    print("created plates")
    return print(cur.lastrowid)  # how much values


def get_plate(conn, connection, quantity=200, search=False, data='', hour='',
              plate=''):

    print("-------------------",data, hour, plate)
    database_show_page = []
    db_for_page = ''
    cur = conn.cursor()
    stmt = select(text('* FROM plates'))

    if not search:
        with connection as conn:
            for row in conn.execute(stmt):

                if row[0] < quantity:
                    db_for_page += "<tr>"
                    for i in row:
                        db_for_page += "<td>" + str(i) + "</td>"
                    db_for_page += "</tr>"
                    database_show_page.append(row)
        conn.commit()
        return db_for_page

    else:
        print("++++++++++++++++++", data, hour, plate)
        with connection as conn:
            for row in conn.execute(stmt):

                if data == row[1] and hour == row[2] and plate == row[3]:
                    db_for_page += "<tr>"
                    for i in row:
                        db_for_page += "<td>" + str(i) + "</td>"
                    db_for_page += "</tr>"
                    database_show_page.append(row)
                    print("all values")

                if data:
                    if plate:
                        if not hour:
                            if data == row[1] and plate == row[3]:
                                db_for_page += "<tr>"
                                for i in row:
                                    db_for_page += "<td>" + str(i) + "</td>"
                                db_for_page += "</tr>"
                                database_show_page.append(row)
                                print("bez hour")

                if data:
                    if not plate:
                        if not hour:
                            if data == row[1]:
                                db_for_page += "<tr>"
                                for i in row:
                                    db_for_page += "<td>" + str(i) + "</td>"
                                db_for_page += "</tr>"
                                database_show_page.append(row)
                                print("only data")
                if plate:
                    if not data:
                        if not hour:
                            if plate == row[3]:
                                db_for_page += "<tr>"
                                for i in row:
                                    db_for_page += "<td>" + str(i) + "</td>"
                                db_for_page += "</tr>"
                                database_show_page.append(row)
                                print("only plate")

        conn.commit()
        return db_for_page


def drop_plate(conn, data):
    cur = conn.cursor()
    sql = 'SELECT * FROM plate;'

# update
# i pobaw sie z selectem, aby zwracalo ci na tablicy zamiast tego dicta
# sqlalchemy ORM
# user = User(name=fdf)
# db.session.add(user)
# db.session.commit()

# alembic revision --autogenerate -m "Intial tables"
# alembic downgrade base
# alembic upgrade head

# git checkout -b database_connect
# git commit -m something
# git push -u origin name_branch
# source venv/local/bin/activate

# git pull origin master
# git status
# pip freeze > requirements.txt
# sqlite3 name
