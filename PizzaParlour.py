import flask
import json
import csv
from flask import Flask, request, jsonify

app = Flask("Assignment 2")


@app.route('/pizza')
def welcome_pizza():
    return 'Welcome to Pizza Planet!'

# Order Id counter
order_id = 0
# Dictionary for all orders
orders = {}

# Load menu from menu.json
with open('menu.json') as json_file:
    menu = json.load(json_file)

# Check whether the order is validate or not
def isValid(order):
    if "Drink" not in order or "Pizza" not in order:
        return False
    for pizza in order["Pizza"]:
        for option in pizza:
            if "Size" not in option or "Type" not in option or "Topping" not in option:
                return False
    return True


# Transfer json file to csv file
def json_to_csv(json):
    result = ""
    return result

# Return an order id
@app.route('/pizza/get_id', methods=['GET'])
def get_id():
    global order_id
    order_id += 1
    return order_id

# Submit an order
@app.route('/pizza/submit_order', methods=['POST'])
def submit_order():
    content = request.get_json()
    if not isValid(content):
        status_code = flask.Response(status=404)
        return status_code
    orders[str(order_id)] = content
    return orders


@app.route('/pizza/get_order/<order_id>', methods=['GET'])
def get_order(order_id):
    if str(order_id) not in orders:
        status_code = flask.Response(status=404)
        return status_code
    else:
        return orders[order_id]

#
@app.route('/pizza/update_order/<order_id>', methods=['POST'])
def update_order(order_id):
    if str(order_id) not in orders:
        status_code = flask.Response(status=404)
        return status_code
    content = request.get_json()
    orders[order_id] = content
    return "Update Done"


@app.route('/pizza/cancle_order/<order_id>', methods=['DELETE'])
def cancel_order(order_id):
    if str(order_id) not in orders:
        status_code = flask.Response(status=404)
        return status_code
    del orders[order_id]
    return "Cancel Done"


@app.route('/pizza/get_menu/<item>', methods=['GET'])
def get_menu(item):
    if item == 'FULL':
        return menu
    elif item not in menu:
        status_code = flask.Response(status=404)
        return status_code
    else:
        return str(menu[item])


@app.route('/pizza/delivery/<order_id>/<method>', methods=['GET'])
def delivery(order_id, method):
    if method == 'PickUp' or 'InHouse':
        return "Thank you for ordering"
    elif method == 'UberEats':
        content = request.get_json()
        uber_order = {
            'Address': content['address'],
            'Order Details': orders[order_id],
            'Order Number': order_id
        }
        return jsonify(uber_order)
    elif method == 'Foodora':
        foodra_order = {
            'Address': "aaa",
            'Order Details': orders[order_id],
            'Order Number': order_id
        }
        return json_to_csv(foodra_order)


if __name__ == "__main__":
    app.run()
