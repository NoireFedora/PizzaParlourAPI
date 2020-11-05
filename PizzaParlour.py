import flask
from flask import Flask, request

app = Flask("Assignment 2")

@app.route('/pizza')
def welcome_pizza():
    return 'Welcome to Pizza Planet!'

order_id = 0
orders = {}

def print_receipt(orders):
    for order in orders:
        print(orders[order])
        print("\n")

@app.route('/pizza/submit_order', methods = ['POST'])
def submit_order():
    global order_id
    pizza_id = 1
    order_id += 1
    content = request.get_json()
    orders[order_id] = content
    for pizza in orders[order_id]["Pizza"]:
        pizza["ID"] = pizza_id
        pizza_id += 1
    print_receipt(orders)
    return orders

@app.route('/pizza/update_order/<order_id>', methods = ['POST'])
def update_order(order_id):
    if order_id not in orders:
        status_code = flask.Response(status=404)
        return status_code
    content = request.get_json()
    for order in orders:
        for modified in content:
            if modified == order:
                orders[order] = content
    print(orders)
    return "Update Done"

@app.route('/pizza/cancle_order/<order_id>', methods = ['POST'])
def cancel_order(order_id):
    if order_id not in orders:
        status_code = flask.Response(status=404)
        return status_code
    del orders[order_id]
    print(orders)
    return "Cancel Done"

if __name__ == "__main__":
    app.run()
