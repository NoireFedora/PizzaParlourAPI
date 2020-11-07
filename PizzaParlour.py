import flask
import json
from flask import Flask, request, jsonify

app = Flask("Assignment 2")


@app.route('/pizza')
def welcome_pizza():
    return 'Welcome to Pizza Planet!'

# Object Order
class Order:
    def __init__(self, order_id, pizza_list=None, drink_list=None, address=None, delivery=None):
        self.order_id = order_id
        self.pizza_list = pizza_list
        self.drink_list = drink_list
        self.address = address
        self.delivery = delivery

# Object Pizza
class Pizza:
    def __init__(self, size, type, topping):
        self.size = size
        self.type = type
        self.topping = topping

# Order Id counter
order_id = 0
# List for all orders
orders = {}
# Attributes of a pizza
pizza_attr = ["Id", "Size", "Type", "Toppings"]

# Load menu from menu.json
with open('menu.json') as json_file:
    menu = json.load(json_file)

# Check whether a pizza request is valid or not
def isvalidpizza(pizza, format):

    # A json file (dictionary) sample:
    #{"Id": 1,
    #"Size": 12,
    #"Type": "Neapolitan",
    #"Toppings": ["cheese", "apple", "meat"]}
    if format == "json":
        if len(pizza) != 4:
            return False
        if "Id" not in pizza or "Size" not in pizza or "Type" not in pizza or "Toppings" not in pizza:
            return False
        if pizza["Size"] not in menu or pizza["Type"] not in menu:
            return False
        for topping in pizza["Toppings"]:
            if topping not in menu:
                return False
        return True

    # A csv file (string) sample:
    # "Id,Size,Type,Toppings \n 1,12,Neapolitan,cheese:apple:meat"
    elif format == "csv":
        temp = pizza.split("\n")
        attrs = temp[0].split(",")
        vals = temp[1].split(",")
        if len(attrs) != 4 or len(vals) != 4:
            return False
        for attr in attrs:
            if attr not in pizza_attr:
                return False
        for val in vals[1:-1]:
            if val not in menu:
                return False
        toppings = vals[-1].split(":")
        for topping in toppings:
            if topping not in menu:
                return False
        return True

# Check whether a drinks request is valid or not
def isvaliddrinks(drinks, format):

    # A json file (dictionary) sample:
    # {"Id": 1,
    #  "Drink": ["coke", "spirit"]}
    if format == "json":
        if len(drinks) != 2:
            return False
        if "Id" not in drinks or "Drink" not in drinks:
            return False
        for drink in drinks["Drink"]:
            if drink not in menu:
                return False
        return True

    # A csv file (string) sample:
    # "Id,Drink /n 1,spirit:coke:water"
    elif format == "csv":
        temp = drinks.split("\n")
        attrs = temp[0].split(",")
        vals = temp[1].split(",")
        if len(attrs) != 2 or len(vals) != 2:
            return False
        if "Drink" not in attrs:
            return False
        drinklist = vals[-1].split(":")
        for drink in drinklist:
            if drink not in menu:
                return False
        return True

# Return an order id
@app.route('/pizza/get_id', methods=['GET'])
def get_id():
    global order_id
    order_id += 1
    return str(order_id)
<<<<<<< HEAD

# Submit a pizza request
@app.route('/pizza/submit_pizza/<delivery>', methods=['POST'])
def submit_pizza(delivery):

    if delivery == "Foodora":
        if not isvalidpizza(request, "csv"):
            status_code = flask.Response(status=404)
            return status_code
        temp = request.split("\n")
        values = temp[1].split(",")
        id = values[0]
        if not id in orders:
            orders[id] = Order(id)
            orders[id].pizza_list = [Pizza(values[1], values[2], values[3].split(":"))]
            if delivery is None:
                orders[id].delivery = delivery
        else:
            if orders[id].pizza_list is None:
                orders[id].pizza_list = [Pizza(values[1], values[2], values[3].split(":"))]
            else:
                orders[id].pizza_list += [Pizza(values[1], values[2], values[3].split(":"))]
        return "Pizza Request Accepted"

    if delivery == "Uber" or delivery == "PizzaP" or delivery == "Instore":
        content = request.get_json()
        if not isvalidpizza(content, "json"):
            status_code = flask.Response(status=404)
            return status_code
        id = content["Id"]
        if not id in orders:
            orders[id] = Order(id)
            orders[id].pizza_list = [Pizza(content["Size"], content["Type"], content["Toppings"])]
            if delivery is None:
                orders[id].delivery = delivery
        else:
            if orders[id].pizza_list is None:
                orders[id].pizza_list = [Pizza(content["Size"], content["Type"], content["Toppings"])]
            else:
                orders[id].pizza_list += [Pizza(content["Size"], content["Type"], content["Toppings"])]
        return "Pizza Request Accepted"
=======
>>>>>>> e81fb24df0d446386050c0a36b6181cc6187b871

    else:
        status_code = flask.Response(status=404)
        return status_code

# Submit drinks request
@app.route('/pizza/submit_drinks/<delivery>', methods=['POST'])
def submit_drinks(delivery):

    if delivery == "Foodora":
        if not isvaliddrinks(request, "csv"):
            status_code = flask.Response(status=404)
            return status_code
        temp = request.split("\n")
        values = temp[1].split(",")
        id = values[0]
        if not id in orders:
            orders[id] = Order(id)
            orders[id].drink_list = values[1].split(":")
            if delivery is None:
                orders[id].delivery = delivery
        else:
            if orders[id].drink_list is None:
                orders[id].drink_list = values[1].split(":")
            else:
                orders[id].drink_list += values[1].split(":")
        return "Drinks Request Accepted"

    if delivery == "Uber" or delivery == "PizzaP" or delivery == "Instore":
        content = request.get_json()
        if not isvaliddrinks(content, "json"):
            status_code = flask.Response(status=404)
            return status_code
        id = content["Id"]
        if not id in orders:
            orders[id] = Order(id)
            orders[id].drink_list = content["Drink"]
            if delivery is None:
                orders[id].delivery = delivery
        else:
            if orders[id].drink_list is None:
                orders[id].drink_list = content["Drink"]
            else:
                orders[id].drink_list += content["Drink"]
        return "Drinks Request Accepted"

    else:
        status_code = flask.Response(status=404)
        return status_code

# Submit address
@app.route('/pizza/submit_address/<delivery>', methods=['POST'])
def submit_address(delivery):

    if delivery == "Foodora":
        temp = request.split("\n")
        attrs = temp[0].split(",")
        values = temp[1].split(",")
        id = values[0]
        if len(attrs) != 2 or len(values) != 2:
            status_code = flask.Response(status=404)
            return status_code
        if not id in orders:
            orders[id] = Order(id)
            orders[id].address = values[1]
            if delivery is None:
                orders[id].delivery = delivery
        else:
            orders[id].address = values[1]

        return "Drinks Request Accepted"

    if delivery == "Uber" or delivery == "PizzaP" or delivery == "Instore":
        content = request.get_json()
        if "Id" not in content or "Address" not in content:
            status_code = flask.Response(status=404)
            return status_code
        id = content["Id"]
        if not id in orders:
            orders[id] = Order(id)
            orders[id].address = content["Address"]
            if delivery is None:
                orders[id].delivery = delivery
        else:
            orders[id].address = content["Address"]

        return "Drinks Request Accepted"

    else:
        status_code = flask.Response(status=404)
        return status_code

# Cancel an order
@app.route('/pizza/cancel_order/<order_id>', methods=['DELETE'])
def cancel_order(order_id):
    if str(order_id) not in orders:
        status_code = flask.Response(status=404)
        return status_code
    del orders[order_id]
    return "Cancel Done"

# Get menu
@app.route('/pizza/get_menu/<item>', methods=['GET'])
def get_menu(item):
    if item == "FULL":
        return menu
    elif item not in menu:
        status_code = flask.Response(status=404)
        return status_code
    else:
        return str(menu[item])


if __name__ == "__main__":
    app.run()
