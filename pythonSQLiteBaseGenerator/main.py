import os
import sqlite3, random
from datetime import datetime, timedelta

if os.path.exists('sales.db'):
    os.remove('sales.db')

connection = sqlite3.connect('sales.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE,
        product TEXT,
        quantity INTEGER,
        price FLOAT
    )
''')

def generate_data(num_rows):
    products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
    start_date = datetime(2010, 1, 1).date()

    for i in range(num_rows):
        date = start_date + timedelta(days=random.randint(0, 365*12))
        product = random.choice(products)
        quantity = random.randint(1, 10)
        price = round(random.uniform(10.0, 100.0), 2)

        yield (date, product, quantity, price)

num_rows = 1000  # количество строк для генерации
data = generate_data(num_rows)

cursor.executemany('''
    INSERT INTO sales (date, product, quantity, price)
    VALUES (?, ?, ?, ?)
''', data)

connection.commit()
connection.close()