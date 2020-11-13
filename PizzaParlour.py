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
    def __init__(self, order_id: str, pizza_list: list = None, drink_list: list = None, address: str = None,
                 delivery: str = None):
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
        # Whether this Order is submitted or not. If not, it is a temporary Order.
        self.submitted = False


# Object Pizza
class Pizza:
    def __init__(self, size: str, type: str, toppings: list):
        # The Size of this Pizza
        self.size = size
        # The Type of this Pizza
        self.type = type
        # The list contains all Toppings in this Pizza
        self.toppings = toppings


# Order Id Counter
order_id_counter = 0
# The list contains all Orders
orders = {}
# Attributes of a Pizza
pizza_attr = ["Id", "Size", "Type", "Toppings"]

# Load menu from menu.json
with open('menu.json') as json_file:
    menu = json.load(json_file)


# Check whether a pizza request is valid or not
def isvalidpizza(pizza, file_type):
    """
    A json file (dictionary) sample:
    {"Id": 1,
    "Size": "Small",
    "Type": "Neapolitan",
    "Toppings": ["Chicken", "Beef", "Mushrooms"]}

    A csv file (string) sample:
    "Id,Size,Type,Toppings\n1,Small,Neapolitan,[Chicken,Beef,Mushrooms]"
    """
    if file_type == "json":
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

    elif file_type == "csv":
        temp = pizza.split("\n")
        attrs = temp[0].split(",")
        vals = temp[1].split(",")
        if len(attrs) != 4 or len(vals) < 4:
            return False
        if "\r" in attrs[-1]:
            attrs[-1] = attrs[-1].strip("\r")
        if "[" in vals[3]:
            vals[3] = vals[3].strip("[")
        if "]" in vals[-1]:
            vals[-1] = vals[-1].strip("]")
        for attr in attrs:
            if attr not in pizza_attr:
                return False
        for val in vals[1:]:
            if val not in menu:
                return False
        return True


# Check whether a drinks request is valid or not
def isvaliddrinks(drinks, file_type):
    # A json file (dictionary) sample:
    # {"Id": 1,
    #  "Drink": ["Coke", "Pepsi"]}
    if file_type == "json":
        if len(drinks) != 2:
            return False
        if "Id" not in drinks or "Drink" not in drinks:
            return False
        for drink in drinks["Drink"]:
            if drink not in menu:
                return False
        return True

    # A csv file (string) sample:
    # "Id,Drink\n1,[Coke,Pepsi]"
    elif file_type == "csv":
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


# Return an Order Id
@app.route('/pizza/get_id', methods=['GET'])
def get_id():
    global order_id_counter
    order_id_counter += 1
    return str(order_id_counter)


# Submit a Pizza to a temporary Order (Create if not exist, Add if exist)
@app.route('/pizza/submit_pizza/<delivery>', methods=['POST'])
def submit_pizza(delivery):
    if delivery == "Foodora":
        pizza = request.data.decode('utf-8')
        if not isvalidpizza(pizza, "csv"):
            return "Pizza Request is not valid"
        temp = pizza.split("\n")
        values = temp[1].split(",")
        order_id = values[0]
        if "[" in values[3]:
            values[3] = values[3].strip("[")
        if "]" in values[-1]:
            values[-1] = values[-1].strip("]")
        if not (order_id in orders):
            orders[order_id] = Order(order_id)
            orders[order_id].pizza_list = [Pizza(values[1], values[2], values[3:])]
            if orders[order_id].delivery is None:
                orders[order_id].delivery = delivery
        else:
            if orders[order_id].pizza_list is None:
                orders[order_id].pizza_list = [Pizza(values[1], values[2], values[3:])]
            else:
                orders[order_id].pizza_list += [Pizza(values[1], values[2], values[3:])]
        orders[order_id].total += menu[values[1]] + menu[values[2]]
        for topping in values[3:]:
            orders[order_id].total += menu[topping]
        return "Pizza Request Received"

    if delivery == "Uber" or delivery == "PizzaP" or delivery == "Instore":
        content = json.loads(request.data)
        if not isvalidpizza(content, "json"):
            return "Pizza Request is not valid"
        order_id = str(content["Id"])
        if not (order_id in orders):
            orders[order_id] = Order(order_id)
            orders[order_id].pizza_list = [Pizza(content["Size"], content["Type"], content["Toppings"])]
            if orders[order_id].delivery is None:
                orders[order_id].delivery = delivery
        else:
            if orders[order_id].pizza_list is None:
                orders[order_id].pizza_list = [Pizza(content["Size"], content["Type"], content["Toppings"])]
            else:
                orders[order_id].pizza_list += [Pizza(content["Size"], content["Type"], content["Toppings"])]
        orders[order_id].total += menu[content["Size"]] + menu[content["Type"]]
        for topping in content["Toppings"]:
            orders[order_id].total += menu[topping]
        return "Pizza Request Received"

    else:
        status_code = flask.Response(status=404)
        return status_code


# Submit Drinks to a temporary Order (Create if not exist, Add if exist)
@app.route('/pizza/submit_drinks/<delivery>', methods=['POST'])
def submit_drinks(delivery):
    if delivery == "Foodora":
        drink = request.data.decode('utf-8')
        if not isvaliddrinks(drink, "csv"):
            return "Drink Request is not valid"
        temp = drink.split("\n")
        values = temp[1].split(",")
        order_id = values[0]
        if "[" in values[1]:
            values[1] = values[1].strip("[")
        if "]" in values[-1]:
            values[-1] = values[-1].strip("]")
        if not (order_id in orders):
            orders[order_id] = Order(order_id)
            orders[order_id].drink_list = values[1:]
            if orders[order_id].delivery is None:
                orders[order_id].delivery = delivery
        else:
            if orders[order_id].drink_list is None:
                orders[order_id].drink_list = values[1:]
            else:
                orders[order_id].drink_list += values[1:]
        for drink in orders[order_id].drink_list:
            orders[order_id].total += menu[drink]
        return "Drinks Request Received"

    if delivery == "Uber" or delivery == "PizzaP" or delivery == "Instore":
        content = json.loads(request.data)
        if not isvaliddrinks(content, "json"):
            return "Drink Request is not valid"
        order_id = str(content["Id"])
        if not (order_id in orders):
            orders[order_id] = Order(order_id)
            orders[order_id].drink_list = content["Drink"]
            if orders[order_id].delivery is None:
                orders[order_id].delivery = delivery
        else:
            if orders[order_id].drink_list is None:
                orders[order_id].drink_list = content["Drink"]
            else:
                orders[order_id].drink_list += content["Drink"]
        for drink in orders[order_id].drink_list:
            orders[order_id].total += menu[drink]
        return "Drinks Request Received"

    else:
        status_code = flask.Response(status=404)
        return status_code


# Submit an Address to a temporary Order (Create if not exist, Cover if exist)
@app.route('/pizza/submit_address/<delivery>', methods=['POST'])
def submit_address(delivery):
    if delivery == "Foodora":
        pizza = request.data.decode('utf-8')
        temp = pizza.split("\n")
        attrs = temp[0].split(",")
        values = temp[1].split(",")
        order_id = values[0]
        if len(attrs) != 2 or len(values) != 2:
            return "Address Request is not valid"
        if not (order_id in orders):
            orders[order_id] = Order(order_id)
            orders[order_id].address = values[1]
            if orders[order_id].delivery is None:
                orders[order_id].delivery = delivery
        else:
            orders[order_id].address = values[1]

        return "Address Request Received"

    if delivery == "Uber" or delivery == "PizzaP" or delivery == "Instore":
        content = json.loads(request.data)
        if "Id" not in content or "Address" not in content:
            return "Address Request is not valid"
        order_id = str(content["Id"])
        if not (order_id in orders):
            orders[order_id] = Order(order_id)
            orders[order_id].address = content["Address"]
            if orders[order_id].delivery is None:
                orders[order_id].delivery = delivery
        else:
            orders[order_id].address = content["Address"]

        return "Address Request Received"

    else:
        status_code = flask.Response(status=404)
        return status_code


# Pop a target Pizza
@app.route('/pizza/pop_single_pizza/<order_id>/<index>', methods=['GET', 'Delete'])
def pop_single_pizza(order_id, index):
    if order_id not in orders:
        return "Order Id does not exist"
    pizza_list = orders[order_id].pizza_list
    if int(index) > len(pizza_list) - 1:
        return "Index is not valid"
    pizza = pizza_list[int(index)]
    json_output = {"Size": pizza.size, "Type": pizza.type, "Toppings": pizza.toppings}
    orders[order_id].total -= menu[pizza.size] + menu[pizza.type]
    for topping in pizza.toppings:
        orders[order_id].total -= menu[topping]
    del pizza_list[int(index)]
    return jsonify(json_output)


# Delete a drink
@app.route('/pizza/delete_drink/<order_id>/<index>', methods=['DELETE'])
def delete_drink(order_id, index):
    if order_id not in orders:
        return "Order Id does not exist"
    drink_list = orders[order_id].drink_list
    if int(index) > len(drink_list) - 1:
        return "Index is not valid"
    drink = drink_list[int(index)]
    orders[order_id].total -= menu[drink]
    del drink_list[int(index)]
    return "Drink Deleted"


# Cancel an Order
@app.route('/pizza/cancel_order/<order_id>', methods=['DELETE'])
def cancel_order(order_id):
    if order_id not in orders:
        return "Order Id does not exist"
    del orders[order_id]
    return "Cancel Request Received"


# Get Menu
@app.route('/pizza/get_menu/<item>', methods=['GET'])
def get_menu(item):
    if item == "FULL":
        return menu
    elif item not in menu:
        return "Item does not exist"
    else:
        return str(menu[item])


# Get a string contains all Pizza in target Order
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
            count) + "\n    Size: " + pizza.size + "\n   Type: " + pizza.type + "\n   Toppings: "
        for topping in pizza.toppings:
            checkout += menu[topping]
            result += topping + " "
        result += "\n"
        result += "Price: {}".format(checkout)
    return result


# Get a string contains all Drinks in target Order
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


# Check whether the Order is valid or not. If valid, then submit and return a string with all information of this Order.
@app.route('/pizza/check_order/<order_id>', methods=['POST'])
def check_order(order_id):
    if order_id not in orders:
        return "Order Id does not exist"
    order = orders[order_id]
    if order.delivery is None:
        return "No Delivery Method"
    if order.pizza_list is None and order.drink_list is None:
        return "Nothing Ordered"
    if order.delivery != "Instore":
        if order.address is None:
            return "No Address"
    order.submitted = True
    result = "Order {} Submitted\n".format(order_id)
    count = 0
    for pizza in order.pizza_list:
        count += 1
        result += " Pizza {}:".format(
            count) + "\n      Size: " + pizza.size + "\n       Type: " + pizza.type + "\n       Topping: "
        for topping in pizza.toppings:
            result += topping + " "
        result += "\n"
    result += " Drink: "
    for drink in order.drink_list:
        result += drink + " "
    result += "\n" + "Total Price: {}".format(order.total)
    return result


# Add a new Pizza Type with Price into Menu. Cover if exist.
@app.route('/pizza/add_menu/<name>/<price>', methods=['POST'])
def add_menu(name, price):
    menu[name] = int(price)
    with open('menu.json', "w") as json_file_w:
        json.dump(menu, json_file_w)
    return "Name:{}({}) is added to menu".format(name, price)


if __name__ == "__main__":
    app.run()
