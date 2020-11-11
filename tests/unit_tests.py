from PizzaParlour import app

def test_pizza():
    response = app.test_client().get('/pizza')

    assert response.status_code == 200
    assert response.data == b'Welcome to Pizza Planet!'

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
    csv = "Id,Size,Type,Toppings\n1,Small,Neapolitan,[Chicken,Beef,Mushrooms]"
    response = app.test_client().post('/pizza/submit_pizza/Foodora', data=csv)
    assert response.status_code == 200
    assert response.data == b'Pizza Request Received'

def test_submit_pizza_json():
    json = {"Id": 1, "Size": "Small", "Type": "Neapolitan", "Toppings": ["Chicken", "Beef", "Mushrooms"]}
    response = app.test_client().post('/pizza/submit_pizza/Uber', json=json)
    assert response.status_code == 200
    assert response.data == b'Pizza Request Received'

def test_submit_drinks_csv():
    csv = "Id,Drink\n1,[Coke,Pepsi]"
    response = app.test_client().post('/pizza/submit_drinks/Foodora', data=csv)
    assert response.status_code == 200
    assert response.data == b'Drinks Request Received'

def test_submit_drinks_json():
    json = {"Id": 1, "Drink":["Coke", "Pepsi"]}
    response = app.test_client().post('/pizza/submit_drinks/Uber', json=json)
    assert response.status_code == 200
    assert response.data == b'Drinks Request Received'

def test_submit_address_csv():
    csv = "Id,Drink\n1,UofT"
    response = app.test_client().post('/pizza/submit_address/Foodora', data=csv)
    assert response.status_code == 200
    assert response.data == b'Address Request Received'

def test_submit_address_json():
    json = {"Id": 1, "Address":"UofT"}
    response = app.test_client().post('/pizza/submit_address/Uber', json=json)
    assert response.status_code == 200
    assert response.data == b'Address Request Received'

def test_delete_drink():
    json = {"Id": 1, "Drink": ["Coke", "Pepsi"]}
    app.test_client().post('/pizza/submit_drinks/Uber', json=json)
    response = app.test_client().delete('/pizza/delete_drinks/1/0')
    assert response.status_code == 200
    assert response.data == b'Drink Deleted'
