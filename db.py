import sqlite3
from collections import namedtuple
db = sqlite3.connect(':memory:')
db.execute('create table persons (id integer, name text, profession text)')
pers = namedtuple('Person', ['id', 'name', 'profession'])
ppl = [pers(1, 'Juan', 'professor'), pers(2, 'WTF', 'engineer'), pers(24, 'klk', 'doctor')]

for p in ppl:
    db.execute('insert into persons values (?,?,?)', p)

ppl = db.execute('Select * from persons')
print(ppl.fetchall())
