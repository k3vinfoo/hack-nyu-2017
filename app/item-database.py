import sqlite3 as lite
import sys

item = (
    ('7572000081', 'Water', 8.13),
    ('7572000082', 'Soda', 1.4),
)

con = lite.connect('item.db')

with con:
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS items")
    cur.execute("CREATE TABLE items(barcode TEXT, item_name TEXT, cost REAL)")
    cur.executemany("INSERT INTO items VALUES(?, ?, ?)", item)