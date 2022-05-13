import sqlite3

#Creates an SQLite database. Light weight database that does not require a server.
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

#A Note on development
#Moving forward, a more robust database will be needed, for SQL we can use PostGres.
#If items have more variability than we can consider using a NoSQL database e.g (DynamoDB) if read/write performance matters