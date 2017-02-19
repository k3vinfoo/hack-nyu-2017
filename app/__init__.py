from flask import *
import sqlite3
import sys
import os
from os import path
from os import listdir
import sqlite3
import pypyodbc
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

DATABASE = "app/people.db"

app = Flask(__name__) 
app.config.from_object(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

def connect_db():
    return sqlite3.connect(DATABASE)

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
    g.db = connect_db()
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

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
