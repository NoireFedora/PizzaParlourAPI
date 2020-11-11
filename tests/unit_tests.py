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

def test_submit_pizza():
    # Foodora
    foodora = "Id,Size,Type,Toppings" \
              "1,Small,Neapolitan,[Chicken,Beef,Mushrooms]"
    response = app.test_client().post('/pizza/submit_pizza/Foodora', txt=foodora)
    assert response.status_code == 200
    assert response.data == b'Pizza Request Received'