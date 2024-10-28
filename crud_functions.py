import sqlite3


def initiate_db():
    with sqlite3.connect('initiate.db') as db:
        cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Products(
     id integer PRIMARY KEY,
     title text NOT NULL,
     description text ,
     price integer NOT NULL);
     """)

    for i in range(1, 5):
        cursor.execute('INSERT INTO Products (title, description, price)VALUES(?,?,?)',
                       (f'Продукт{i}', f'описание{i}', i * 100))

    db.commit()
    db.close()
    with sqlite3.connect('initiate2.db') as db2:
        cursor = db2.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Users(
     id integer PRIMARY KEY,
     username text NOT NULL,
     email text NOT NULL ,
     age integer NOT NULL,
     balance integer NOT NULL);
     """)
    db2.commit()


def add_user(username, email, age):
    with sqlite3.connect('initiate2.db') as db2:
        cursor = db2.cursor()
    cursor.execute('INSERT INTO Users (username, email,age,balance)VALUES(?,?,?,?)',
                   (f'{username}', f'{email}', f'{age}', 1000,))
    db2.commit()


def is_included(username):
    with sqlite3.connect('initiate2.db') as db2:
        cursor = db2.cursor()
    check_user = cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    db2.commit()

    if check_user.fetchone() is None:
        return False
    else:
        return True


def get_all_products():
    with sqlite3.connect('initiate.db') as db:
        cursor = db.cursor()
    cursor.execute("SELECT * FROM Products")

    db.commit()

    return cursor.fetchall()
