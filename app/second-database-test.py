import sqlite3 as lite
import sys

people = (
    ('ajf500', 'hello2016', .99),
    ('kt5678', 'hello2016', 40.00),
    ('tf9101', 'hello2016', 50.00),
    ('a', 'a', 10000.00),
)

con = lite.connect('people.db')

with con:
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS reps")
    cur.execute("CREATE TABLE reps(rep_name TEXT, password TEXT, amount REAL)")
    cur.executemany("INSERT INTO reps VALUES(?, ?, ?)", people)
