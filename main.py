import mysql.connector
from flask import Flask, request

app = Flask(__name__)

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="customer_database"
)

cursor = conn.cursor()

@app.route('/', methods=['GET'])  
def index():
    return "Hello, world!"

@app.route('/getcustomers', methods=['GET'])
def get_customers():
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    return {"customers": customers}

@app.route('/getcustomer/<int:customer_id>', methods=['GET'])
def get_customer_by_id(customer_id):
    cursor.execute("SELECT name, email, phone, address FROM customers WHERE customer_id = %s", (customer_id,))
    customer = cursor.fetchone()
    return {"name": customer[0], "email": customer[1], "phone": customer[2], "address": customer[3]}

@app.route('/getorders', methods=['GET'])
def get_orders():
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    return {"orders": orders}

@app.route('/getorder/<int:order_id>', methods = ['GET'])
def get_orders_by_id(order_id):
    cursor.execute("SELECT customer_id, order_date, total_amount FROM orders WHERE order_id = %s", (order_id,))
    order = cursor.fetchone()
    return{"customer_id": order[0], "order_date": order[1], "total_amount": order[2]}

@app.route('/getorderbycus_Id/<int:customer_id>', methods=['GET'])
def get_order_cus_id(customer_id):
    cursor.execute("SELECT order_id, order_date, total_amount FROM orders WHERE customer_id = %s", (customer_id,))
    orders = cursor.fetchall()
    return{"orders": orders}

@app.route('/createcustomer', methods=['POST'])
def create_a_new_customer():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address')
    cursor.execute("INSERT INTO customers (name, email, phone, address) VALUES (%s, %s, %s, %s)", (name, email, phone, address))
    conn.commit()
    return{"message" : "customer created"}

@app.route('/createorder', methods=['POST'])
def create_a_new_order():
    data = request.get_json()
    customer_id = data.get('customer_id')
    order_date = data.get('order_date')
    total_amount = data.get('total_amount')
    cursor.execute("INSERT INTO orders (customer_id, order_date, total_amount) VALUES (%s, %s, %s)", (customer_id, order_date, total_amount))
    conn.commit()
    return{"message" : "order created"}

@app.route('/updatecustomer/<int:customer_id>', methods=['PUT'])
def update_customer_details(customer_id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address')
    cursor.execute("UPDATE customers SET name = %s, email = %s, phone = %s, address = %s WHERE customer_id = %s", (name, email, phone, address, customer_id))
    conn.commit()
    return {"message": "customer updated"}

@app.route('/updateorder/<int:order_id>', methods=['PUT'])
def update_order_detaild(order_id):
    data = request.get_json()
    customer_id = data.get("customer_id")
    order_date = data.get("order_date")
    total_amount = data.get("total_amount")
    cursor.execute("UPDATE orders SET customer_id = %s, order_date = %s, total_amount = %s WHERE order_id = %s", (customer_id, order_date, total_amount, order_id))
    conn.commit()
    return{"message" : "order updated"}

@app.route('/deletecustomer/<customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    cursor.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
    conn.commit()
    return {"message": "customer deleted"}

@app.route('/deleteorder/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
    conn.commit()
    return {"message": "order deleted"}

if __name__ == '__main__':
    app.run(debug=True)

