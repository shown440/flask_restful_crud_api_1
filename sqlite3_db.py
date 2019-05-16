import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

# int=INTEGER. but if we need auto incremented id then we have to write INTEGER
create_table_users = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table_users)
print("users table created successfully...")

create_table_items = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
cursor.execute(create_table_items)
print("items table created successfully...")

insert_items="INSERT INTO items VALUES('Bus', 99.99)"
cursor.execute(insert_items)
print("data inserted into items table successfully...")

connection.commit()
connection.close()
