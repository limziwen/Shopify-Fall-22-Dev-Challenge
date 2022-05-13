from flask import Flask, render_template, request, send_from_directory
import sqlite3 as sql
from initDb import createDb

app = Flask(__name__)

#returns the home page, where user can input items
@app.route('/')
def home():
   return render_template('home.html')

#returns all valid objects in inventory
@app.route('/update')
def update():
   try:
      con = sql.connect("database.db")
      con.row_factory = sql.Row
      cur = con.cursor()
      cur.execute("select * from items where visible = 1")
      con.commit()
      rows = cur.fetchall()
   except Exception as e:
      return render_template('errorpage.html', errorMsg = str(e))
   finally:
      con.close()

   return render_template('update.html', rows = rows)

#updates singular item in database
@app.route('/updateItem', methods = ['POST'])
def updateItem():
   if request.method == 'POST':
      try:
         name = request.form['name']
         quantity = request.form['quantity']
         con = sql.connect("database.db")
         con.row_factory = sql.Row
         
         cur = con.cursor()
         # prevent sql injections using query parameters
         cur.execute("select * from items where name=?", (name,))
         con.commit()
         row = cur.fetchone()

         if row is None:
            return render_template('errorpage.html', errorMsg = "Item not found")
         else:
            cur.execute("update items set quantity = ? where name = ?", (quantity, name,))    
            con.commit()
      except Exception as e:
         return render_template('errorpage.html', errorMsg = str(e))
      finally:
         con.close()
   return update()

#deletes single item from database
@app.route('/delete', methods = ['POST'])
def delete():
   if request.method == 'POST':
      try:
         name = request.form['name']
         comment = request.form['comment']
         con = sql.connect("database.db")
         con.row_factory = sql.Row
         
         cur = con.cursor()
         cur.execute("select * from items where name=?", (name,))
         con.commit()
         row = cur.fetchone()

         if row is None:
            return render_template('error.html', message = "Item not found")
         else:
            cur.execute("update items set visible = 0, deletionComments = ? where name = ?", (comment, name,))
            con.commit()
      except Exception as e:
         print(e)
         return render_template('errorpage.html', errorMsg = str(e))
      finally:
         con.close()
   return update()

#insert item into database
@app.route('/insert',methods = ['POST', 'GET'])
def insert():
   if request.method == 'POST':
      print("recieved ", request.form)
      try:
         name = request.form['name']
         quantity = request.form['quantity']
         with sql.connect("database.db") as con:
            cur = con.cursor()
            #prevent sql injections using query parameters
            cur.execute("insert into items(name,quantity,visible,deletionComments) values(?,?,?,?)", (name, quantity, 1, ""))
            con.commit()
      except Exception as e:
         return render_template('errorpage.html', errorMsg = str(e))
      finally:
         con.close()
   
   return update()

#display all items in database with visible = 0
@app.route("/deletelist")
def deletelist():
   try:
      con = sql.connect("database.db")
      con.row_factory = sql.Row
      cur = con.cursor()
      cur.execute("select * from items where visible = 0")
      con.commit()
      rows = cur.fetchall()
   except Exception as e:
      return render_template('errorpage.html', errorMsg = str(e))
   finally:
      con.close()

   return render_template("deletedlist.html",rows = rows)

#update visible to 1 for recieving item
@app.route("/restore", methods = ['POST'])
def restoreItem():
   if request.method == 'POST':
      try:
         name = request.form['name']
         con = sql.connect("database.db")
         con.row_factory = sql.Row
         
         cur = con.cursor()
         cur.execute("select * from items where name = ?", (name,))
         con.commit()
         row = cur.fetchone()
         if row is None:
            return render_template('errorpage.html', errorMsg = "item cannot be restored, not found")
         else:
            cur.execute("update items set visible = 1 where name = ?", (name,))
            con.commit()
      except Exception as e:
         return render_template('errorpage.html', errorMsg = str(e))
      finally:
         con.close()
   return update()

if __name__ == '__main__':
   createDb()
   app.run(debug = True)


# Notes on code:
# Query parameters to prevent sql injections.
# try/except block to catch any errors that may occur, including database errors (duplicate item entries, connection failures, etc.)
# finally block to close the connection to the database.