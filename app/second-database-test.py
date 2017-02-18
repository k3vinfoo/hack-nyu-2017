import sqlite3 as lite
import sys

people = (
    ('BO1234', 'hello2016', 20),
    ('KT5678', 'hello2016', 40),
    ('TF9101', 'hello2016', 50),
)

con = lite.connect('people.db')

with con:
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS reps")
    cur.execute("CREATE TABLE reps(rep_name TEXT, password TEXT, amount INT)")
    cur.executemany("INSERT INTO reps VALUES(?, ?, ?)", people)
