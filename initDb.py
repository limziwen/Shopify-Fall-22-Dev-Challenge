import sqlite3


def createDb():
    try:
        conn = sqlite3.connect('database.db')
        print("Opened database successfully")

        conn.execute('CREATE TABLE items (name TEXT NOT NULL PRIMARY KEY, quantity INTEGER NOT NULL, visible BOOLEAN, deletionComments TEXT)')
        print("Table created successfully")
        conn.close()
    except Exception as e:
        print(e)
    return