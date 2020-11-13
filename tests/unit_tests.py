import json

from PizzaParlour import app


def test_pizza():
    response = app.test_client().get('/pizza')

    assert response.status_code == 200
    assert response.data == b'Welcome to Pizza Planet!'

"""
Unit Tests for API
"""

with open('menu.json') as json_file:
    menu = json.load(json_file)

valid_pizza_csv      = "Id,Size,Type,Toppings\n1,Small,Neapolitan,[Chicken,Beef,Mushrooms]"
valid_pizza_json     = {"Id": 1, "Size": "Small", "Type": "Neapolitan", "Toppings": ["Chicken", "Beef", "Mushrooms"]}
valid_drinks_csv     = "Id,Drink\n1,[Coke,Pepsi]"
valid_drinks_json    = {"Id": 1, "Drink":["Coke", "Pepsi"]}
valid_address_csv    = "Id,Drink\n1,UofT"
valid_address_json   = {"Id": 1, "Address":"UofT"}

invalid_pizza_csv    = "Id,Size,Type,Toppings\n1,Small,Neapolitan,[Chicken,Beef,Ramen]"
invalid_pizza_json   = {"Id": 1, "Size": "Monster", "Type": "Neapolitan", "Toppings": ["Chicken", "Beef", "Mushrooms"]}
invalid_drinks_csv   = "Id,Drink\n1,[Coke,Milk]"
invalid_drinks_json  = {"Drink":["Coke", "Pepsi"]}
invalid_address_csv  = "Address\nUofT"
invalid_address_json = {"Id": 1, "School":"UofT"}

valid_address_json2  = {"Id": 2, "Address":"UofT"}
valid_drinks_json5   = {"Id": 5, "Drink":["Coke", "Pepsi"]}

def test_get_id():
    response = app.test_client().get('/pizza/get_id')
    assert response.status_code == 200
    assert response.data == b'1'
    response = app.test_client().get('/pizza/get_id')
    assert response.status_code == 200
    assert response.data == b'2'
    response = app.test_client().get('/pizza/get_id')
    assert response.status_code == 200
    assert response.data == b'3'

def test_submit_pizza_csv():
    # Valid
    response = app.test_client().post('/pizza/submit_pizza/Foodora', data=valid_pizza_csv)
    assert response.status_code == 200
    assert response.data == b'Pizza Request Received'
    response = app.test_client().post('/pizza/submit_pizza/Foodora', data=valid_pizza_csv)
    assert response.status_code == 200
    assert response.data == b'Pizza Request Received'
    # Invalid
    response = app.test_client().post('/pizza/submit_pizza/Foodora', data=invalid_pizza_csv)
    assert response.status_code == 200
    assert response.data == b'Pizza Request is not valid'
    # 404
    response = app.test_client().post('/pizza/submit_pizza/FOD', data=valid_pizza_csv)
    assert response.status_code == 404

def test_submit_pizza_json():
    # Valid
    response = app.test_client().post('/pizza/submit_pizza/Uber', json=valid_pizza_json)
    assert response.status_code == 200
    assert response.data == b'Pizza Request Received'
    response = app.test_client().post('/pizza/submit_pizza/Uber', json=valid_pizza_json)
    assert response.status_code == 200
    assert response.data == b'Pizza Request Received'
    # Invalid
    response = app.test_client().post('/pizza/submit_pizza/Uber', json=invalid_pizza_json)
    assert response.status_code == 200
    assert response.data == b'Pizza Request is not valid'
    # 404
    response = app.test_client().post('/pizza/submit_pizza/FOD', data=valid_pizza_json)
    assert response.status_code == 404

def test_submit_drinks_csv():
    # Valid
    response = app.test_client().post('/pizza/submit_drinks/Foodora', data=valid_drinks_csv)
    assert response.status_code == 200
    assert response.data == b'Drinks Request Received'
    response = app.test_client().post('/pizza/submit_drinks/Foodora', data=valid_drinks_csv)
    assert response.status_code == 200
    assert response.data == b'Drinks Request Received'
    # Invalid
    response = app.test_client().post('/pizza/submit_drinks/Foodora', data=invalid_drinks_csv)
    assert response.status_code == 200
    assert response.data == b'Drink Request is not valid'
    # 404
    response = app.test_client().post('/pizza/submit_drinks/FOD', data=valid_drinks_csv)
    assert response.status_code == 404

def test_submit_drinks_json():
    # Valid
    response = app.test_client().post('/pizza/submit_drinks/Uber', json=valid_drinks_json)
    assert response.status_code == 200
    assert response.data == b'Drinks Request Received'
    response = app.test_client().post('/pizza/submit_drinks/Uber', json=valid_drinks_json)
    assert response.status_code == 200
    assert response.data == b'Drinks Request Received'
    # Invalid
    response = app.test_client().post('/pizza/submit_drinks/Uber', json=invalid_drinks_json)
    assert response.status_code == 200
    assert response.data == b'Drink Request is not valid'
    # 404
    response = app.test_client().post('/pizza/submit_drinks/FOD', data=valid_drinks_json)
    assert response.status_code == 404

def test_submit_address_csv():
    # Valid
    response = app.test_client().post('/pizza/submit_address/Foodora', data=valid_address_csv)
    assert response.status_code == 200
    assert response.data == b'Address Request Received'
    response = app.test_client().post('/pizza/submit_address/Foodora', data=valid_address_csv)
    assert response.status_code == 200
    assert response.data == b'Address Request Received'
    # Invalid
    response = app.test_client().post('/pizza/submit_address/Foodora', data=invalid_address_csv)
    assert response.status_code == 200
    assert response.data == b'Address Request is not valid'
    # 404
    response = app.test_client().post('/pizza/submit_address/FOD', data=valid_address_csv)
    assert response.status_code == 404

def test_submit_address_json():
    # Valid
    response = app.test_client().post('/pizza/submit_address/Uber', json=valid_address_json)
    assert response.status_code == 200
    assert response.data == b'Address Request Received'
    response = app.test_client().post('/pizza/submit_address/Uber', json=valid_address_json)
    assert response.status_code == 200
    assert response.data == b'Address Request Received'
    response = app.test_client().post('/pizza/submit_address/Uber', json=valid_address_json2)
    assert response.status_code == 200
    assert response.data == b'Address Request Received'
    # Invalid
    response = app.test_client().post('/pizza/submit_address/Uber', json=invalid_address_json)
    assert response.status_code == 200
    assert response.data == b'Address Request is not valid'
    # 404
    response = app.test_client().post('/pizza/submit_address/FOD', data=valid_address_json)
    assert response.status_code == 404

def test_pop_single_pizza():
    # Valid
    result = {"Size": "Small", "Type": "Neapolitan", "Toppings": ["Chicken", "Beef", "Mushrooms"]}
    app.test_client().post('/pizza/submit_pizza/Uber', json=valid_pizza_json)
    response = app.test_client().get('/pizza/pop_single_pizza/1/0')
    assert response.status_code == 200
    assert json.loads(response.data) == result
    # Invalid
    app.test_client().post('/pizza/submit_pizza/Uber', json=valid_pizza_json)
    response = app.test_client().get('/pizza/pop_single_pizza/10/0')
    assert response.status_code == 200
    assert response.data == b"Order Id does not exist"
    app.test_client().post('/pizza/submit_pizza/Uber', json=valid_pizza_json)
    response = app.test_client().get('/pizza/pop_single_pizza/1/10')
    assert response.status_code == 200
    assert response.data == b"Index is not valid"

def test_delete_drink():
    # Valid
    app.test_client().post('/pizza/submit_drinks/Uber', json=valid_drinks_json)
    response = app.test_client().delete('/pizza/delete_drink/1/0')
    assert response.status_code == 200
    assert response.data == b'Drink Deleted'
    # Invalid
    response = app.test_client().delete('/pizza/delete_drink/10/0')
    assert response.status_code == 200
    assert response.data == b"Order Id does not exist"
    response = app.test_client().delete('/pizza/delete_drink/1/20')
    assert response.status_code == 200
    assert response.data == b"Index is not valid"

def test_cancel_order():
    # Valid
    app.test_client().post('/pizza/submit_pizza/Uber', json=valid_pizza_json)
    response = app.test_client().delete('/pizza/cancel_order/1')
    assert response.status_code == 200
    assert response.data == b'Cancel Request Received'
    # Invalid
    response = app.test_client().delete('/pizza/cancel_order/1')
    assert response.status_code == 200
    assert response.data == b"Order Id does not exist"

def test_get_menu():
    # Valid
    response_FULL = app.test_client().get('/pizza/get_menu/FULL')
    assert response_FULL.status_code == 200
    assert json.loads(response_FULL.data) == menu
    response_item = app.test_client().get('/pizza/get_menu/Beef')
    assert response_item.status_code == 200
    assert response_item.data == b'4'
    # Invalid
    response_invalid = app.test_client().get('/pizza/get_menu/Ramen')
    assert response_invalid.status_code == 200
    assert response_invalid.data == b"Item does not exist"

def test_get_pizza_list():
    # Valid
    app.test_client().post('/pizza/submit_pizza/Foodora', data=valid_pizza_csv)
    response = app.test_client().get('/pizza/get_pizza_list/1')
    assert response.status_code == 200
    result = b'Pizza 1:\n    Size: Small\n   Type: Neapolitan\n   Toppings: Chicken Beef Mushrooms \nPrice: 14'
    assert response.data == result
    # Invalid
    response = app.test_client().get('/pizza/get_pizza_list/10')
    assert response.status_code == 200
    assert response.data == b"Order Id does not exist"

def test_get_drink_list():
    # Valid
    app.test_client().post('/pizza/submit_drinks/Foodora', data=valid_drinks_csv)
    response = app.test_client().get('/pizza/get_drink_list/1')
    assert response.status_code == 200
    assert response.data == b'Drink: Coke Pepsi \nTotal Price: 5.0'
    # Invalid
    response = app.test_client().get('/pizza/get_drink_list/10')
    assert response.status_code == 200
    assert response.data == b"Order Id does not exist"

def test_check_order():
    # Valid
    app.test_client().post('/pizza/submit_address/Foodora', data=valid_address_csv)
    response = app.test_client().post('/pizza/check_order/1')
    assert response.status_code == 200
    result = b'Order 1 Submitted\n Pizza 1:\n      Size: Small\n       Type: Neapolitan\n       Topping: Chicken Beef Mushrooms \n Drink: Coke Pepsi \nTotal Price: 19.0'
    assert response.data == result
    # Invalid
    response = app.test_client().post('/pizza/check_order/10')
    assert response.status_code == 200
    assert response.data == b"Order Id does not exist"
    app.test_client().post('/pizza/submit_address/Instore', json=valid_address_json2)
    response = app.test_client().post('/pizza/check_order/2')
    assert response.status_code == 200
    assert response.data == b"Nothing Ordered"
    app.test_client().post('/pizza/submit_drinks/Uber', json=valid_drinks_json5)
    response = app.test_client().post('/pizza/check_order/5')
    assert response.status_code == 200
    assert response.data == b"No Address"

def test_add_menu():
    response = app.test_client().post('/pizza/add_menu/Fungi/5')
    assert response.status_code == 200
    assert response.data == b'Type:Fungi(5) is added to menu'

