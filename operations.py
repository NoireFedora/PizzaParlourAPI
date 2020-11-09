import requests
import switcher
import json
import connection
def creat_order(delivery_method, Address):
    # first get the order number from api
    r = requests.get('http://127.0.0.1:5000/pizza/get_id')
    order_id = r.content.decode("utf-8")

    print(order_id)
    while True:

        # ask user to select pizza size
        pizza_size = "Invalid OP"
        while pizza_size == "Invalid OP":
            pizza_size = input("please Select pizza size\n1: Small\n2: Medium\n3: Large\n4: Extra_large\n")
            pizza_size = switcher.pizza_size_option(pizza_size)
            if pizza_size == "Invalid OP":
                print("invalid input please try again\n")

        # ask user for pizza type
        pizza_type = ""
        while pizza_type == "":
            pizza_type = input("please enter pizza type\n")
            if pizza_type == "":
                print("you need to select one type\n")

        # ask user for pizza Topping
        cur_topping = "Invalid OP"
        pizza_topping = []
        while cur_topping == "Invalid OP":
            cur_topping = input("please Select pizza size\n1: olives\n2: tomatoes\n3: mushrooms\n4: jalapenos\n5: "
                                "chicken\n6: "
                                "beef\n7: pepperoni\n")
            cur_topping = switcher.pizza_topping_option(cur_topping)
            if pizza_topping == "Invalid OP":
                print("invalid input please try again\n")
            else:
                pizza_topping.append(cur_topping)
                cur_topping = "Invalid OP"
                cont = input("add one more topping? Y for Yes, other input for NO\n")
                if cont != "Y":
                    break

        # now we have a pizza trying to send this pizza to the api and store it
        if delivery_method != "Foodora":
            order = {
                "Id": order_id,
                "Size": pizza_size,
                "Type": pizza_type,
                "Toppings": pizza_topping
            }

            pizza_json = json.dumps(order)
            server_code = connection.send('http://127.0.0.1:5000/pizza/submit_pizza/'+delivery_method, pizza_json)

            if server_code.status_code == 404:
                print("smothing wrong with you pizza, please enter the pizza again")
            else:
                print(server_code.text)
                cont = input("add more pizza? Y for Yes, other input for NO\n")
                if cont != "Y":
                    break
        else:
            new_list=','.join(pizza_topping)
            order = "Id,Size,Type,Toppings\n"+order_id +","+pizza_size+","+pizza_size+",["+str(new_list)+"]"
            server_code = connection.send('http://127.0.0.1:5000/pizza/submit_pizza/' + delivery_method, order)
            if server_code.status_code == 404:
                print("smothing wrong with you pizza, please enter the pizza again")
            else:
                print(server_code.text)
                cont = input("add more pizza? Y for Yes, other input for NO\n")
                if cont != "Y":
                    break

    # now ask for drink
    cur_drink = "Invalid OP"
    drinks = []
    while cur_drink == "Invalid OP":
        cur_drink = input("please Select drink \n1: Coke\n2: Diet Coke\n3: Coke_Zero\n4: Pepsi\n5: "
                            "Diet_Pepsi\n6: "
                            "Dr.Pepper\n7: Water\n8: Juice")
        cur_drink = switcher.drink_option(cur_drink)
        if drinks == "Invalid OP":
            print("invalid input please try again\n")
        else:
            drinks.append(cur_drink)
            cur_drink = "Invalid OP"
            cont = input("add one more topping? Y for Yes, other input for NO\n")
            if cont != "Y":
                break
    # now we have a pizza trying to send this pizza to the api and store it
    if delivery_method != "Foodora":
        order = {
            "Id": order_id,
            "Drink": drinks,
        }

        pizza_json = json.dumps(order)
        print(pizza_json)
        server_code = connection.send('http://127.0.0.1:5000/pizza/submit_drinks/'+delivery_method, pizza_json)

        if server_code.status_code == 404:
            print("smothing wrong with you drink, please enter the drink again")
        else:
            print(server_code.text)

    else:
        new_list=','.join(drinks)
        order = "Id,Drink\n"+order_id + ",["+str(new_list)+"]"
        print(order)
        server_code = connection.send('http://127.0.0.1:5000/pizza/submit_drinks/' + delivery_method, order)
        if server_code.status_code == 404:
            print("smothing wrong with you drink, please enter the drink again")
        else:
            print(server_code.text)


    return None
