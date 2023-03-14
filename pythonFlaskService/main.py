import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)

# Роут для добавления записи о продаже
@app.route('/sales/', methods=['POST'])
def add_sale():
    try:
        data = request.json
        date = data['date']
        product = data['product']
        quantity = data['quantity']
        price = data['price']
        with sqlite3.connect('sales.db') as con:
            cur = con.cursor()
            cur.execute('INSERT INTO sales(date, product, quantity, price) VALUES (?, ?, ?, ?)', (date, product, quantity, price))
            con.commit()
        return jsonify({'success': True, 'message': 'Запись о продаже успешно добавлена.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Роут для получения данных о продажах за период
@app.route('/sales/', methods=['GET'])
def get_sales():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        with sqlite3.connect('sales.db') as con:
            cur = con.cursor()
            cur.execute('SELECT * FROM sales WHERE date BETWEEN ? AND ?', (start_date, end_date))
            rows = cur.fetchall()
        sales_list = [{'id': row[0], 'date': row[1], 'product': row[2], 'quantity': row[3], 'price': row[4]} for row in rows]
        return jsonify({'success': True, 'sales': sales_list})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run()
