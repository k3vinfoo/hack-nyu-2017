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
purchasedb = "app/purchase.db"

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
        global userid
        userid = user[0]
        return render_template('camera.html')

# Send barcode to Database
@app.route('/p', methods=['POST'])
def addRegion():
    findthing(request.form['bc'], userid)
    return render_template('camera.html')

@app.route('/purchases', methods=['POST'])
def show_purchases():
    history = connect_db(purchasedb)
    history_query = history.execute('SELECT * FROM purchases WHERE userid = ?', (userid,))
    total = 0
    return render_template('purchases.html', purchases = history_query.fetchall(), total = total)

def charge_account(item_cost, netid):
    account = connect_db(peopledb)
    person_query = account.execute('SELECT amount FROM reps WHERE rep_name = ?', (netid,))
    user_balance = person_query.fetchone()
    new_balance = user_balance[0] - item_cost
    account.execute('UPDATE reps SET amount = ? WHERE rep_name = ?', (new_balance, netid))
    account.commit()

def findthing (barcodenum, netid):
    store = connect_db(itemdb)
    itemquery = store.execute('SELECT cost, item_name FROM items WHERE barcode = ?', (barcodenum,))
    item = itemquery.fetchone()
    purchase_history(userid, item[1], item[0])
    if item is None:
        print("Item not found")
    else:
        charge_account(item[0], netid)

def purchase_history(netid, name, cost):
    transactions = connect_db(purchasedb)
    transaction_query = transactions.execute('INSERT INTO purchases VALUES (?, ?, ?)', (netid, name, cost))
    transactions.commit()

# findthing("7572000081", 'a')
# findthing("7572000082", 'a')

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)