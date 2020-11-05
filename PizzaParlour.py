import flask
import json
import csv
from flask import Flask, request

app = Flask("Assignment 2")


@app.route('/pizza')
def welcome_pizza():
    return 'Welcome to Pizza Planet!'


order_id = 0
orders = {}

with open('menu.json') as json_file:
    menu = json.load(json_file)

def print_receipt(orders):
    for order in orders:
        print(orders[order])
        print("\n")


@app.route('/pizza/submit_order', methods=['POST'])
def submit_order():
    global order_id
    order_id += 1
    content = request.get_json()
    orders[str(order_id)] = content
    print_receipt(orders)
    return orders


@app.route('/pizza/get_order/<order_id>', methods=['GET'])
def get_order(order_id):

    if str(order_id) not in orders:
        status_code = flask.Response(status=404)
        return status_code
    else:
        return orders[order_id]


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

@app.route('/pizza/delivery/<method>', methods=['POST'])
def delivery(method):
    if method == 'PickUp':
        return "Thank you for ordering"
    elif method == 'InHouse' or method == 'UberEats':
        content = request.get_json()
        for order in orders:
             if order == content["order_id"]:
                content["order_details"] = orders[order]
                content["Method"] = method
                orders[order]["Delivery"] = content
        return content
    elif method == 'Foodora':


if __name__ == "__main__":
    app.run()
