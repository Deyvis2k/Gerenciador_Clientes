from tinydb import TinyDB

database = TinyDB('db.json', indent= 4)
database.default_table_name = 'admin'