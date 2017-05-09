import sqlite3
from collections import namedtuple
db = sqlite3.connect(':memory:')
db.execute('create table persons (id integer, name text, profesion text)')
db.execute('create table cities (id_cities integer, city text)')

pers = namedtuple('Person', ['id', 'name', 'profession'])
city = namedtuple('info', ['id', 'ciudad'])
ppl = [pers(38, 'Juan', 'professor'), pers(2, 'WTF', 'engineer'), pers(24, 'klk', 'doctor'), pers(3, 'Juan', 'janitor')]
cities = [city(38, 'Las Palms')]

for p in ppl:
    db.execute('insert into persons values (?,?,?)', p)

for c in cities:
    db.execute('insert into cities values (?,?)', c)

# db.execute('UPDATE persons SET profesion = "wasa" WHERE name = "Juan" AND id=1')
ppl = db.execute('select name from persons,cities WHERE id=id_cities')

print(ppl.fetchall())