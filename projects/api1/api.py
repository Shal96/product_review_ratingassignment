import traceback
import flask
import sqlite3
from flask import Flask, render_template, request, jsonify

#Database Creation
conn = sqlite3.connect('database.db')
print ("Opened database successfully")
#conn.execute('DROP TABLE productinfo2')
conn.execute('CREATE TABLE IF NOT EXISTS  productinfo2 (product_id TEXT, Reviews TEXT, Ratings TEXT, Status TEXT)')
print ("Table created successfully")
conn.close()

#FLASK APP
app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route("/")
def index():
"""
Arguments : None
Returns: Home Page
"""
    return "Home Page"

@app.route('/query')
def query():
"""
Arguments = none
Returns = Query HTML template containing form to input pid, review and rating
"""
   return render_template('query.html')
   

@app.route('/prodrec',methods = ['POST'])
def prodrec():
"""
Arguments: none
Returns : Results template showing results after inserting data into Query form
"""

   if request.method == 'POST':
      try:
         pid = request.form['pid']
         review = request.form['review']
         rating = request.form['rating']

         con = sqlite3.connect('database.db')
         cur = con.cursor()
         
         cur.execute("INSERT INTO productinfo2 (product_id,Reviews,Ratings, Status) VALUES (?,?,?,?)",(pid, review, rating, "New_entry")) #Insert Data into database
         #cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
         #print(cur.fetchall())
         
         con.commit()
         
         msg = "Records successfully added"
         return render_template("results.html",msg = msg)
         con.close()
      except:
         #con.rollback()
         
         msg = traceback.print_exc()
         print(msg)
         return render_template("results.html",msg = msg)
         
      
      #finally:
       #  return render_template("results.html",msg = msg)
        # conn.close()
 

@app.route('/list', methods=['GET'])
def list():
"""
Arguments :
Returns :  List HTML template containing table for data
"""
   con = sqlite3.connect("database.db")
   con.row_factory = sqlite3.Row
   cur = con.cursor()
   cur.execute("SELECT Ratings, COUNT(*) FROM productinfo2 GROUP BY Ratings")
     
   rows = cur.fetchall()
   
   for row in rows:
       count=row["COUNT(*)"]
       print("The rating_count  : " + str(count))
       rate = row["Ratings"]
       print("The type of rating : " + str(rate))

   #for row in rows:
    #    print(row["COUNT(*)"])
    #    print(row["Ratings"])
    #   print(row.keys())
   cur.execute("UPDATE productinfo2 SET Status = 'Processed_entry' WHERE Status = 'New_entry'")# Once the sorting/pre processing is done update the status from new entry to processed entry
   con.close()
   return render_template("list.html",rows = rows)

   
@app.route('/api_all', methods=['GET'])
def api_all():
"""
Arguments :
Returns: api exposing list of count of a particular rating(eg: 3 counts of rating 5) and a list of typeof rating(eg: 5)
"""
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT Ratings, COUNT(*) FROM productinfo2 GROUP BY Ratings")
        
        rows = cur.fetchall()
        count=[]
        rate=[]
        for row in rows:
            count.append(row["COUNT(*)"])
            print("The rating_count  : " + str(count))
            rate.append(row["Ratings"])
            print("The type of rating : " + str(rate))

        cur.execute("UPDATE productinfo2 SET Status = 'Processed_entry' WHERE Status = 'New_entry'")  
        con.close()
        return jsonify(count, rate)
        
    
if __name__ == '__main__':
   app.run(debug = True)