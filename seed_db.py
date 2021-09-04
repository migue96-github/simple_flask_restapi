import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table_query_users = "CREATE TABLE IF NOT EXISTS users (id int, username text, password text)"

create_table_query_items = "CREATE TABLE IF NOT EXISTS items (name text, price float)"

cursor.execute(create_table_query_users)
cursor.execute(create_table_query_items)

items = [
    ('piano', 16.99),
    ('guitar', 10.50)
]

users = [
    (1, 'manolo', '123'),
    (2, 'pepe', '123'),
    (3, 'migue', '123')
]

insert_item_query = "INSERT INTO items VALUES (?, ?)"
insert_user_query = "INSERT INTO users VALUES (?, ?, ?)"

cursor.executemany(insert_item_query, items)
cursor.executemany(insert_user_query, users)

connection.commit()

connection.close()
