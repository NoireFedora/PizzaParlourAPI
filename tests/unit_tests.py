import json

from PizzaParlour import app

def test_pizza():
    response = app.test_client().get('/pizza')

    assert response.status_code == 200
    assert response.data == b'Welcome to Pizza Planet!'

with open('menu.json') as json_file:
    menu = json.load(json_file)

valid_pizza_csv      = "Id,Size,Type,Toppings\n1,Small,Neapolitan,[Chicken,Beef,Mushrooms]"
valid_pizza_json     = {"Id": 1, "Size": "Small", "Type": "Neapolitan", "Toppings": ["Chicken", "Beef", "Mushrooms"]}
valid_drinks_csv     = "Id,Drink\n1,[Coke,Pepsi]"
valid_drinks_json    = {"Id": 1, "Drink":["Coke", "Pepsi"]}
valid_address_csv    = "Id,Drink\n1,UofT"
valid_address_json   = {"Id": 1, "Address":"UofT"}

invalid_pizza_csv    = "Id,Size,Type,Toppings\n1,Small,Neapolitan,[Chicken,Beef,Ramen]"
invalid_pizza_json   = {"Id": 1, "Size": "Small", "Type": "Neapolitan", "Toppings": ["Chicken", "Beef", "Ramen"]}
invalid_drinks_csv   = "Id,Drink\n1,[Coke,Milk]"
invalid_drinks_json  = {"Id": 1, "Drink":["Coke", "Milk"]}
invalid_address_csv  = "Address\nUofT"
invalid_address_json = {"Address":"UofT"}

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
    # Invalid
    response = app.test_client().post('/pizza/submit_pizza/Foodora', data=invalid_pizza_csv)
    assert response.status_code == 200
    assert response.data == b'Pizza Request is not valid'

def test_submit_pizza_json():
    # Valid
    response = app.test_client().post('/pizza/submit_pizza/Uber', json=valid_pizza_json)
    assert response.status_code == 200
    assert response.data == b'Pizza Request Received'
    # Invalid
    response = app.test_client().post('/pizza/submit_pizza/Uber', json=invalid_pizza_json)
    assert response.status_code == 200
    assert response.data == b'Pizza Request is not valid'

def test_submit_drinks_csv():
    # Valid
    response = app.test_client().post('/pizza/submit_drinks/Foodora', data=valid_drinks_csv)
    assert response.status_code == 200
    assert response.data == b'Drinks Request Received'
    # Invalid
    response = app.test_client().post('/pizza/submit_drinks/Foodora', data=invalid_drinks_csv)
    assert response.status_code == 200
    assert response.data == b'Drink Request is not valid'

def test_submit_drinks_json():
    # Valid
    response = app.test_client().post('/pizza/submit_drinks/Uber', json=valid_drinks_json)
    assert response.status_code == 200
    assert response.data == b'Drinks Request Received'
    # Invalid
    response = app.test_client().post('/pizza/submit_drinks/Uber', json=invalid_drinks_json)
    assert response.status_code == 200
    assert response.data == b'Drink Request is not valid'

def test_submit_address_csv():
    # Valid
    response = app.test_client().post('/pizza/submit_address/Foodora', data=valid_address_csv)
    assert response.status_code == 200
    assert response.data == b'Address Request Received'
    # Invalid
    response = app.test_client().post('/pizza/submit_address/Foodora', data=invalid_address_csv)
    assert response.status_code == 200
    assert response.data == b'Address Request is not valid'

def test_submit_address_json():
    # Valid
    response = app.test_client().post('/pizza/submit_address/Uber', json=valid_address_json)
    assert response.status_code == 200
    assert response.data == b'Address Request Received'
    # Invalid
    response = app.test_client().post('/pizza/submit_address/Uber', json=invalid_address_json)
    assert response.status_code == 200
    assert response.data == b'Address Request is not valid'

def test_pop_single_pizza():
    sample = {"Id": 1, "Size": "Small", "Type": "Neapolitan", "Toppings": ["Chicken", "Beef", "Mushrooms"]}
    result = {"Size": "Small", "Type": "Neapolitan", "Toppings": ["Chicken", "Beef", "Mushrooms"]}
    app.test_client().post('/pizza/submit_pizza/Uber', json=sample)
    response = app.test_client().get('/pizza/pop_single_pizza/1/0')
    assert json.loads(response.data) == result

def test_delete_drink():
    json = {"Id": 1, "Drink": ["Coke", "Pepsi"]}
    app.test_client().post('/pizza/submit_drinks/Uber', json=json)
    response = app.test_client().delete('/pizza/delete_drink/1/0')
    assert response.status_code == 200
    assert response.data == b'Drink Deleted'

def test_cancel_order():
    json = {"Id": 1, "Size": "Small", "Type": "Neapolitan", "Toppings": ["Chicken", "Beef", "Mushrooms"]}
    app.test_client().post('/pizza/submit_pizza/Uber', json=json)
    response = app.test_client().delete('/pizza/cancel_order/1')
    assert response.status_code == 200
    assert response.data == b'Cancel Request Received'

def test_get_menu():
    response_FULL = app.test_client().get('/pizza/get_menu/FULL')
    assert response_FULL.status_code == 200
    assert json.loads(response_FULL.data) == menu
    response_item = app.test_client().get('/pizza/get_menu/Beef')
    assert response_item.status_code == 200
    assert response_item.data == b'4'
    response_invalid = app.test_client().get('/pizza/get_menu/Ramen')
    assert response_invalid.status_code == 200
    assert response_invalid.data == b"Item does not exist"

def test_add_menu():
    response = app.test_client().post('/pizza/add_menu/Fungi/5')
    assert response.data == b'Type:Fungi(5) is added to menu'

