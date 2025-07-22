from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Optional: DB init
def init_db():
    conn = sqlite3.connect('bill.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT,
            quantity INTEGER,
            price REAL,
            total REAL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bill', methods=['POST'])
def bill():
    item = request.form['item']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])
    total = quantity * price

    conn = sqlite3.connect('bill.db')
    c = conn.cursor()
    c.execute("INSERT INTO bills (item, quantity, price, total) VALUES (?, ?, ?, ?)",
              (item, quantity, price, total))
    conn.commit()
    conn.close()

    return render_template('bill.html', item=item, quantity=quantity, price=price, total=total)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
