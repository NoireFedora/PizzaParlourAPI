import flask
import json
from flask import Flask, request, jsonify

app = Flask("Assignment 2")

# Start Code
@app.route('/pizza')
def welcome_pizza():
    return 'Welcome to Pizza Planet!'

# Object Order
class Order:
    def __init__(self, order_id:str, pizza_list:list=None, drink_list:list=None, address:str=None, delivery:str=None):
        # The Id of this Order
        self.order_id = order_id
        # The list contains all Pizza in this Order
        self.pizza_list = pizza_list
        # The list contains all Drinks in this Order
        self.drink_list = drink_list
        # Address
        self.address = address
        # Delivery Method
        self.delivery = delivery
        # Total Price of this Order
        self.total = 0

# Object Pizza
class Pizza:
    def __init__(self, size:str, type:str, toppings:list):
        # The Size of this Pizza
        self.size = size
        # The Type of this Pizza
        self.type = type
        # The list contains all Toppings in this Pizza
        self.toppings = toppings

# Order Id Counter
order_id = 0
# The list contains all Orders
orders = {}
# Attributes of a Pizza
pizza_attr = ["Id", "Size", "Type", "Toppings"]

# Load menu from menu.json
with open('menu.json') as json_file:
    menu = json.load(json_file)

# Check whether a pizza request is valid or not
def isvalidpizza(pizza, format):

    """
    A json file (dictionary) sample:
    {"Id": 1,
    "Size": "Small",
    "Type": "Neapolitan",
    "Toppings": ["Chicken", "Beef", "Mushrooms"]}

    A csv file (string) sample:
    "Id,Size,Type,Toppings\n1,Small,Neapolitan,[Chicken,Beef,Mushrooms]"
    """
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

    elif format == "csv":
        temp = pizza.split("\n")
        attrs = temp[0].split(",")
        vals = temp[1].split(",")
        if "\r" in attrs[-1]:
            attrs[-1] = attrs[-1].strip("\r")
        if "[" in vals[3]:
            vals[3] = vals[3].strip("[")
        if "]" in vals[-1]:
            vals[-1] = vals[-1].strip("]")
        if len(attrs) != 4 or len(vals) < 4:
            return False
        for attr in attrs:
            if attr not in pizza_attr:
                return False
        for val in vals[1:]:
            if val not in menu:
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
        if len(attrs) != 2 or len(vals) < 2:
            return False
        if "\r" in attrs[-1]:
            attrs[-1] = attrs[-1].strip("\r")
        if "[" in vals[1]:
            vals[1] = vals[1].strip("[")
        if "]" in vals[-1]:
            vals[-1] = vals[-1].strip("]")
        if "Drink" not in attrs:
            return False
        for drink in vals[1:]:
            if drink not in menu:
                return False
        return True

# Return an order id
@app.route('/pizza/get_id', methods=['GET'])
def get_id():
    global order_id
    order_id += 1
    return str(order_id)

# Submit a pizza request
@app.route('/pizza/submit_pizza/<delivery>', methods=['POST'])
def submit_pizza(delivery):

    if delivery == "Foodora":
        pizza = request.data.decode('utf-8')
        if not isvalidpizza(pizza, "csv"):
            return "Pizza Request is not valid"
        temp = pizza.split("\n")
        values = temp[1].split(",")
        id = values[0]
        if "[" in values[3]:
            values[3] = values[3].strip("[")
        if "]" in values[-1]:
            values[-1] = values[-1].strip("]")
        if not id in orders:
            orders[id] = Order(id)
            orders[id].pizza_list = [Pizza(values[1], values[2], values[3:])]
            if orders[id].delivery is None:
                orders[id].delivery = delivery
        else:
            if orders[id].pizza_list is None:
                orders[id].pizza_list = [Pizza(values[1], values[2], values[3:])]
            else:
                orders[id].pizza_list += [Pizza(values[1], values[2], values[3:])]
        orders[id].total += menu[values[1]] + menu[values[2]]
        for topping in values[3:]:
            orders[id].total += menu[topping]
        return "Pizza Request Received"

    if delivery == "Uber" or delivery == "PizzaP" or delivery == "Instore":
        content = json.loads(request.data)
        if not isvalidpizza(content, "json"):
            return "Pizza Request is not valid"
        id = str(content["Id"])
        if not id in orders:
            orders[id] = Order(id)
            orders[id].pizza_list = [Pizza(content["Size"], content["Type"], content["Toppings"])]
            if orders[id].delivery is None:
                orders[id].delivery = delivery
        else:
            if orders[id].pizza_list is None:
                orders[id].pizza_list = [Pizza(content["Size"], content["Type"], content["Toppings"])]
            else:
                orders[id].pizza_list += [Pizza(content["Size"], content["Type"], content["Toppings"])]
        orders[id].total += menu[content["Size"]] + menu[content["Type"]]
        for topping in content["Toppings"]:
            orders[id].total += menu[topping]
        return "Pizza Request Received"
    else:
        status_code = flask.Response(status=404)
        return status_code

# Submit drinks request
@app.route('/pizza/submit_drinks/<delivery>', methods=['POST'])
def submit_drinks(delivery):

    if delivery == "Foodora":
        drink = request.data.decode('utf-8')
        if not isvaliddrinks(drink, "csv"):
            return "Drink Request is not valid"
        temp = drink.split("\n")
        values = temp[1].split(",")
        id = values[0]
        if "[" in values[1]:
            values[1] = values[1].strip("[")
        if "]" in values[-1]:
            values[-1] = values[-1].strip("]")
        if not id in orders:
            orders[id] = Order(id)
            orders[id].drink_list = values[1:]
            if orders[id].delivery is None:
                orders[id].delivery = delivery
        else:
            if orders[id].drink_list is None:
                orders[id].drink_list = values[1:]
            else:
                orders[id].drink_list += values[1:]
        for drink in orders[id].drink_list:
            orders[id].total += menu[drink]
        return "Drinks Request Received"

    if delivery == "Uber" or delivery == "PizzaP" or delivery == "Instore":
        content = json.loads(request.data)
        if not isvaliddrinks(content, "json"):
            return "Drink Request is not valid"
        id = str(content["Id"])
        if not id in orders:
            orders[id] = Order(id)
            orders[id].drink_list = content["Drink"]
            if orders[id].delivery is None:
                orders[id].delivery = delivery
        else:
            if orders[id].drink_list is None:
                orders[id].drink_list = content["Drink"]
            else:
                orders[id].drink_list += content["Drink"]
        for drink in orders[id].drink_list:
            orders[id].total += menu[drink]
        return "Drinks Request Received"

    else:
        status_code = flask.Response(status=404)
        return status_code

# Submit/Update address
@app.route('/pizza/submit_address/<delivery>', methods=['POST'])
def submit_address(delivery):

    if delivery == "Foodora":
        pizza = request.data.decode('utf-8')
        temp = pizza.split("\n")
        attrs = temp[0].split(",")
        values = temp[1].split(",")
        id = values[0]
        if len(attrs) != 2 or len(values) != 2:
            return "Address Request is not valid"
        if not id in orders:
            orders[id] = Order(id)
            orders[id].address = values[1]
            if orders[id].delivery is None:
                orders[id].delivery = delivery
        else:
            orders[id].address = values[1]

        return "Address Request Received"

    if delivery == "Uber" or delivery == "PizzaP" or delivery == "Instore":
        content = json.loads(request.data)
        if "Id" not in content or "Address" not in content:
            return "Address Request is not valid"
        id = str(content["Id"])
        if not id in orders:
            orders[id] = Order(id)
            orders[id].address = content["Address"]
            if orders[id].delivery is None:
                orders[id].delivery = delivery
        else:
            orders[id].address = content["Address"]

        return "Address Request Received"

    else:
        status_code = flask.Response(status=404)
        return status_code

# Delete a drink
@app.route('/pizza/delete_drink/<order_id>/<index>', methods=['DELETE'])
def delete_drink(order_id, index):
    if order_id not in orders:
        return "Order Id does not exist"
    drink_list = orders[order_id].drink_list
    if int(index) > len(drink_list) - 1:
        return "Index Out Of Range"
    orders[order_id].total -= menu[drink_list[int(index)]]
    del drink_list[int(index)]
    return "Drink Deleted"

# Cancel an order
@app.route('/pizza/cancel_order/<order_id>', methods=['DELETE'])
def cancel_order(order_id):
    if order_id not in orders:
        return "Order Id does not exist"
    del orders[order_id]
    return "Cancel Request Received"

# Get menu
@app.route('/pizza/get_menu/<item>', methods=['GET'])
def get_menu(item):
    if item == "FULL":
        return menu
    elif item not in menu:
        return "Item does not exist"
    else:
        return str(menu[item])

# Get pizza list
@app.route('/pizza/get_pizza_list/<order_id>', methods=['GET'])
def get_pizza_list(order_id):
    if order_id not in orders:
        return "Order Id does not exist"
    order = orders[order_id]
    result = ""
    count = 0
    for pizza in order.pizza_list:
        checkout = 0
        count += 1
        checkout += menu[pizza.size] + menu[pizza.type]
        result += "Pizza {}:".format(
            count) + "\n      Size:" + pizza.size + "\n       Type:" + pizza.type + "\n       Topping:"
        for topping in pizza.toppings:
            checkout += menu[topping]
            result += topping + " "
        result += "\n"
        result += "Price: {}".format(checkout)
    return result

# Get single pizza
@app.route('/pizza/get_single_pizza/<order_id>/<index>', methods=['GET'])
def get_single_pizza(order_id, index):
    if order_id not in orders:
        return "Order Id does not exist"
    pizza_list = orders[order_id].pizza_list
    if int(index) > len(pizza_list) - 1:
        return "Index is not valid"
    pizza = pizza_list[int(index)]
    json = {"Size":pizza.size, "Type":pizza.type, "Toppings":pizza.toppings}
    return jsonify(json)

# Get drink list
@app.route('/pizza/get_drink_list/<order_id>', methods=['GET'])
def get_drink_list(order_id):
    if order_id not in orders:
        return "Order Id does not exist"
    order = orders[order_id]
    result = "Drink: "
    checkout = 0
    for drink in order.drink_list:
        checkout += menu[drink]
        result += drink + " "
    result += "\n" + "Total Price: {}".format(checkout)
    return result

# Check whether the order is valid or not
@app.route('/pizza/check_order/<order_id>', methods=['POST'])
def check_order(order_id):
    if order_id not in orders:
        return "Order Id does not exist"
    order = orders[order_id]
    if order.delivery is None:
        return "No Delivery Method"
    elif order.delivery == "Instore":
        if order.pizza_list is None and order.drink_list is None:
            return "Nothing Ordered"
    else:
        if order.pizza_list is None and order.drink_list is None:
            return "Nothing Ordered"
        if order.address is None:
            return "No Address"
    result = "Order Accepted: {}\n".format(order_id)
    count = 0
    for pizza in order.pizza_list:
        count += 1
        result += " Pizza {}:".format(count) + "\n      Size:" + pizza.size + "\n       Type:" + pizza.type + "\n       Topping:"
        for topping in pizza.toppings:
            result += topping + " "
        result += "\n"
    result += "  Drink: "
    for drink in order.drink_list:
        result += drink + " "
    result += "\n" + "Total Price: {}".format(order.total)
    return result


if __name__ == "__main__":
    app.run()
