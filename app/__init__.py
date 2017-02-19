from flask import *
import sqlite3
import sys
import os
from os import path
from os import listdir
import sqlite3
import pypyodbc
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

peopledb = "app/people.db"
itemdb = "app/item.db"

app = Flask(__name__) 
app.config.from_object(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

def connect_db(database):
    return sqlite3.connect(database)

@app.route("/login.html")
def hello():
    return render_template('login.html', data="hello")

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

def search(dictionary, user):
    if user in dictionary:
        return(True)
    return(False)

@app.route('/')
def home():

    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return("You're already logged in.") # change this to another webpage display shit/info

@app.route('/test', methods = ['POST'])
def user():
    user = request.form['inputNID']
    password = request.form['inputPassword']

    # creates database
    g.db = connect_db(peopledb)
    query = g.db.execute('SELECT * FROM reps WHERE rep_name = ? AND password = ?', (user, password))
    user = query.fetchone()

    if user is None:
        # Non existent
        print("Account non-existent")
        return home(); 
    else:
        # Exists
        print("success!")
        return render_template('camera.html')

def charge_account(item_cost, netid):
    account = connect_db(peopledb)
    person_query = account.execute('SELECT amount FROM reps WHERE rep_name = ?', (netid,))
    user_balance = person_query.fetchone()
    new_balance = user_balance[0] - item_cost
    account.execute('UPDATE reps SET amount = ? WHERE rep_name = ?', (new_balance, netid))
    account.commit()

def findItem(barcodenum, netid):
    store = connect_db(itemdb)
    itemquery = store.execute('SELECT cost FROM items WHERE barcode = ?', (barcodenum,))
    item_cost = itemquery.fetchone()
    if item_cost is None:
        print("Item not found")
    else:
        charge_account(item_cost[0], netid)

findItem("7572000081", 'a')

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
