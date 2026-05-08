from flask import Flask, render_template, request, jsonify, session, redirect, flash
from functools import wraps
import uuid
from datetime import datetime
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'supersecretkey_foodapp_2024'

# ------------------ MYSQL CONFIG ------------------
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'possible24680'
app.config['MYSQL_DB'] = 'orders'

mysql = MySQL(app)

# ------------------ DATA ------------------
USERS = {
    "admin@gmail.com": {
        "name": "Admin",
        "email": "admin@gmail.com",
        "password": "123",
        "addresses": [],
        "phone": ""
    }
}

ORDERS = {}

# ------------------ HELPERS ------------------
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return jsonify({"error": "Login required"}), 401
        return f(*args, **kwargs)
    return decorated

# ------------------ PAGES ------------------
@app.route('/')
def index():
    return render_template('index.html')


# ------------------ LOGIN PAGE ------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['username'].lower()
        password = request.form['password']

        user = USERS.get(email)

        if user and user["password"] == password:
            session["user"] = email
            session["role"] = "admin" if email == "admin@gmail.com" else "user"
            return redirect('/')
        else:
            return "Invalid credentials"

    return render_template("login.html")


# ------------------ LOGOUT ------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# ------------------ ADMIN PANEL ------------------
@app.route('/restaurant-panel')
def restaurant_panel():
    if session.get("role") != "admin":
        return "Unauthorized", 403

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT order_id, status, food_name, quantity
        FROM orders
        ORDER BY id DESC
    """)

    orders = cur.fetchall()
    cur.close()

    return render_template('restaurant_panel.html', orders=orders)


# ------------------ API LOGIN ------------------
@app.route('/api/login', methods=['POST'])
def api_login():
    d = request.json
    email = d.get('email', '').lower()
    password = d.get('password')

    user = USERS.get(email)

    if not user or user['password'] != password:
        return jsonify({"error": "Invalid credentials"}), 401

    session['user'] = email
    session['role'] = "admin" if email == "admin@gmail.com" else "user"

    return jsonify({"success": True})


# ------------------ API LOGOUT ------------------
@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({"success": True})


# ------------------ PLACE ORDER ------------------
@app.route('/api/order/place', methods=['POST'])
@login_required
def place_order():
    d = request.json

    order_id = str(uuid.uuid4())[:8].upper()

    try:
        cur = mysql.connection.cursor()

        cur.execute("""
            INSERT INTO orders(
                order_id,
                customer_email,
                customer_name,
                food_name,
                quantity,
                price,
                address,
                payment,
                status
            )
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            order_id,
            session['user'],
            session['user'],
            d.get('food_name'),
            d.get('quantity'),
            d.get('price'),
            d.get('address'),
            d.get('payment'),
            'confirmed'
        ))

        mysql.connection.commit()
        cur.close()

    except Exception as e:
        print("DB ERROR:", e)

    return jsonify({"success": True, "order_id": order_id})


# ------------------ ORDER STATUS UPDATE ------------------
@app.route('/api/order/<order_id>/next', methods=['POST'])
def next_status(order_id):

    cur = mysql.connection.cursor(dictionary=True)

    cur.execute("SELECT status FROM orders WHERE order_id=%s", (order_id,))
    row = cur.fetchone()

    NEXT = {
        "confirmed": "preparing",
        "preparing": "packed",
        "packed": "on_the_way",
        "on_the_way": "delivered"
    }

    next_step = NEXT.get(row['status'])

    if not next_step:
        return {"msg": "Already delivered"}

    cur.execute(
        "UPDATE orders SET status=%s WHERE order_id=%s",
        (next_step, order_id)
    )
    mysql.connection.commit()
    cur.close()

    return {"new_status": next_step}


# ------------------ RUN ------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)