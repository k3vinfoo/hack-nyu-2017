import sqlite3 as lite
import sys

purchase = ()

con = lite.connect('purchase.db')

with con:
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS purchases")
    cur.execute("CREATE TABLE purchases(userid TEXT, item_name TEXT, item_cost REAL)")
    cur.executemany("INSERT INTO purchases VALUES(?, ?, ?)", purchase)