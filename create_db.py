import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

user_table_query = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
item_table_query = "CREATE TABLE IF NOT EXISTS items (name TEXT PRIMARY KEY, price float)"
cursor.execute(user_table_query)
cursor.execute(item_table_query)

connection.commit()
connection.close()
