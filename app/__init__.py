from flask import *
import sqlite3
import sys
import os
from os import listdir
import sqlite3
import pypyodbc
from flask.ext.login import LoginManager, UserMixin, login_required, login_user, logout_user

DATABASE = "C:/Users/Michelle/Desktop/GitHub/hack-nyu-2017/app/people.db"

app = Flask(__name__) 
app.config.from_object(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

'''
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()
'''

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
        return("You're already logged in.") ## change this to another webpage display shit/info

@app.route('/test', methods = ['POST'])
def user():
    # creates database
    g.db = connect_db()
    cur = g.db.execute('SELECT rep_name, password, amount FROM reps')
    data = {}
    for row in cur.fetchall():
        data[row[0]] = [row[1], row[2]]
    g.db.close()
    
    # data/dictionary {USER: [PW, BALANCE]}
  
    # form verification
    
    #if (request.method == 'GET'):
    #print("hello")
    user = request.form['inputNID']
    password = request.form['inputPassword']
    #print("hello 2")
    print(search(data,user), password, data[user][0])
    if (search(data, user) == True and data[user][0] == password): # if there is an existing user and inputted password matches password key value for user
        print("success!")
    else:
        print("Account non-existent GTFOH")
        return home(); 
    return render_template('camera.html')

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
