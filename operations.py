import requests
import switcher
import json

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
        dictionary = {
            "id": order_id,
            "Size": pizza_size,
            "Type": pizza_type,
            "Toppings": pizza_topping
        }

        pizza_json = json.dumps(dictionary,indent=2)
        print(pizza_json)

    return None
