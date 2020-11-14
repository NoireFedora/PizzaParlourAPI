import requests
import switcher
import json
import connection


def add_Pizza_type():
    # first get user input
    new_item_name = input("please enter the name")
    new_item_price = input("please enter the price in $")
    # send the request
    if new_item_price.isdigit():
        # send these two parameter to the api
        server_code = connection.post('http://127.0.0.1:5000/pizza/add_menu/' + new_item_name + '/' + new_item_price,
                                      "")
        print(server_code.text)
    else:
        print("sorry you price is not in digit")


def creat_order(delivery_method, Address):
    # first get the order number from api
    r = requests.get('http://127.0.0.1:5000/pizza/get_id')
    order_id = r.content.decode("utf-8")

    # print(order_id)
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
            cur_topping = input("please Select pizza topping\n1: olives\n2: tomatoes\n3: mushrooms\n4: jalapenos\n5: "
                                "chicken\n6: "
                                "beef\n7: pepperoni\n")
            cur_topping = switcher.pizza_topping_option(cur_topping)
            if cur_topping == "Invalid OP":
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
            server_code = connection.post('http://127.0.0.1:5000/pizza/submit_pizza/' + delivery_method, pizza_json)

            if server_code.status_code == 404:
                print("smothing wrong with you pizza, please enter the pizza again")
            else:
                print(server_code.text)
                cont = input("add more pizza? Y for Yes, other input for NO\n")
                if cont != "Y":
                    break
        else:
            new_list = ','.join(pizza_topping)
            order = "Id,Size,Type,Toppings\n" + order_id + "," + pizza_size + "," + pizza_type + ",[" + str(
                new_list) + "]"
            server_code = connection.post('http://127.0.0.1:5000/pizza/submit_pizza/' + delivery_method, order)
            if server_code.status_code == 404:
                print("something wrong with you pizza, please enter the pizza again")
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
                          "Dr.Pepper\n7: Water\n8: Juice\n")
        cur_drink = switcher.drink_option(cur_drink)
        if cur_drink == "Invalid OP":
            print("invalid input please try again\n")
        else:
            drinks.append(cur_drink)
            cur_drink = "Invalid OP"
            cont = input("add one more drink? Y for Yes, other input for NO\n")
            if cont != "Y":
                break
    # now we have a pizza trying to send this pizza to the api and store it
    if delivery_method != "Foodora":
        order = {
            "Id": order_id,
            "Drink": drinks,
        }

        pizza_json = json.dumps(order)
        # print(pizza_json)
        server_code = connection.post('http://127.0.0.1:5000/pizza/submit_drinks/' + delivery_method, pizza_json)

        if server_code.status_code == 404:
            print("something wrong with you drink, please enter the drink again")
        else:
            print(server_code.text)

    else:
        new_list = ','.join(drinks)
        order = "Id,Drink\n" + order_id + ",[" + str(new_list) + "]"
        print(order)
        server_code = connection.post('http://127.0.0.1:5000/pizza/submit_drinks/' + delivery_method, order)
        if server_code.status_code == 404:
            print("something wrong with you drink, please enter the drink again")
        else:
            print(server_code.text)

    # print conformation text and also update the delivery address
    if delivery_method != "Foodora":
        address_pass = {
            "Id": order_id,
            "Address": Address
        }
        address_send = json.dumps(address_pass)
        server_code = connection.post('http://127.0.0.1:5000/pizza/submit_address/' + delivery_method, address_send)
    else:
        address_pass = "Id,Address\n" + order_id + "," + Address
        server_code = connection.post('http://127.0.0.1:5000/pizza/submit_address/' + delivery_method, address_pass)

    print(server_code.text)
    print("your order has been created\nyour order ID is:" + order_id + "\n")
    return None


def submit_order():
    # first thing is to ask user for order id
    user_order = input("please enter your order ID :\n")

    # check order id
    server_code = connection.post('http://127.0.0.1:5000/pizza/check_order/' + user_order, "")

    print(server_code.text)


def cancel_order():
    # first thing is to ask user for order id
    user_order = input("please enter your order ID :\n")

    # check order id
    server_code = connection.delete('http://127.0.0.1:5000/pizza/cancel_order/' + user_order, "")

    print(server_code.text)


def pull_menu():
    # first ask user option
    user_order = input("1: Search Item\n2: Full Menu \n")
    if user_order == "2":
        # give user a full menu
        full_menu = connection.get('http://127.0.0.1:5000/pizza/get_menu/FULL', "")
        print("Item                                   Price")
        menu = json.loads(full_menu.text)
        for item in menu:
            print(item, "---------------------------- $", menu[item])
    elif user_order == "1":
        # ask user to enter the name
        search_item = input("please enter the Item you want to search:\n")
        result = connection.get('http://127.0.0.1:5000/pizza/get_menu/' + search_item, "")
        print("$ ", result.text)
    return None


def edit_order(delivery_method):
    # first thing is to ask user for order id
    user_order = input("please enter your order ID :\n")

    # check order id
    server_code = connection.get('http://127.0.0.1:5000/pizza/get_pizza_list/' + user_order, "")
    if server_code.text != "Order Id does not exist":
        while True:
            print(server_code.text)
            # ask if user wanna add pizza delete pizza or edit pizza
            user_decision = input("do you want edit your pizza? A for add, D for delete, E for edit, other for skip")
            if user_decision == "E":
                # ask user which pizza you wanna change
                change_input = input("which pizza do you wanna change? enter pizza number, S for skip this session\n")

                if change_input == "S":
                    # no change any more for this session
                    break
                else:
                    # try to get the target pizza
                    change_input = int(change_input) - 1
                    target_pizza = connection.get(
                        'http://127.0.0.1:5000/pizza/pop_single_pizza/' + user_order + "/" + str(change_input), "")
                    pizza_json = json.loads(target_pizza.text)
                    # print(target_pizza.text)
                    size = pizza_json['Size']
                    topping = pizza_json['Toppings']
                    ptype = pizza_json['Type']
                    # ask if they want to edit pizza size
                    user_decision = input(
                        "please select a new pizza size, \n1: Small\n2: Medium\n3: Large\n4: Extra_large\nother: skip\n")
                    new_size = switcher.pizza_size_option(user_decision)
                    if new_size != "Invalid OP":
                        # switch the new size and the old size
                        print("new size stored")
                    else:
                        new_size = size
                    # ask if they want to edit the pizza topping
                    user_decision = input("do you want to change you pizza topping? Y for yes other for skip")
                    if user_decision == "Y":
                        # ask user for pizza Topping
                        cur_topping = "Invalid OP"
                        pizza_topping = []
                        while cur_topping == "Invalid OP":
                            cur_topping = input(
                                "please Select pizza topping\n1: olives\n2: tomatoes\n3: mushrooms\n4: jalapenos\n5: "
                                "chicken\n6: "
                                "beef\n7: pepperoni\n")
                            cur_topping = switcher.pizza_topping_option(cur_topping)
                            if cur_topping == "Invalid OP":
                                print("invalid input please try again\n")
                            else:
                                pizza_topping.append(cur_topping)
                                cur_topping = "Invalid OP"
                                cont = input("add one more topping? Y for Yes, other input for NO\n")
                                if cont != "Y":
                                    break

                        # replace the old topping with the new topping
                        print("new topping saved")
                    else:
                        pizza_topping = topping
                    # ask if user wanna change pizza type
                    user_decision = input("do you want change your pizza type? Y for yes other for skip\n")
                    if user_decision == "Y":
                        new_pizza_type = ""
                        while new_pizza_type == "":
                            new_pizza_type = input("please enter pizza type\n")
                            if new_pizza_type == "":
                                print("you need to select one type\n")
                    else:
                        new_pizza_type = ptype
                    # here we convert this pizza into json/csv and try to send to backend, if backend return not
                    # valid we send the original pizza back and tell user it is not working now we have a pizza
                    # trying to send this pizza to the api and store it
                    if delivery_method != "Foodora":
                        order = {
                            "Id": user_order,
                            "Size": new_size,
                            "Type": new_pizza_type,
                            "Toppings": pizza_topping
                        }

                        new_pizza_json = json.dumps(order)
                        server_code = connection.post('http://127.0.0.1:5000/pizza/submit_pizza/' + delivery_method,
                                                      new_pizza_json)

                        if server_code.text != "Pizza Request Received":
                            # invalid input we wanna put back the original pizza
                            print("something wrong with you order and the pizza unchanged")
                            order = {
                                "Id": user_order,
                                "Size": size,
                                "Type": ptype,
                                "Toppings": topping
                            }
                            new_pizza_json = json.dumps(order)
                            server_code = connection.post('http://127.0.0.1:5000/pizza/submit_pizza/' + delivery_method,
                                                          new_pizza_json)
                        else:
                            # ask user if wanna edit more pizza?
                            cont = input("Edit more pizza? Y for Yes, other input for NO\n")
                            if cont != "Y":
                                # print(server_code.text)
                                break
                    else:
                        # csv format
                        new_list = ','.join(pizza_topping)
                        order = "Id,Size,Type,Toppings\n" + user_order + "," + new_size + "," + new_pizza_type + ",["+str(new_list) + "]"
                        server_code = connection.post('http://127.0.0.1:5000/pizza/submit_pizza/' + delivery_method,
                                                      order)
                        if server_code.text != "Pizza Request Received":
                            # invalid input we wanna put back the original pizza
                            print("something wrong with you order and the pizza unchanged")
                            new_list = ','.join(topping)
                            order = "Id,Size,Type,Toppings\n" + user_order + "," + size + "," + ptype + ",[" + str(
                                new_list) + "]"
                            server_code = connection.post('http://127.0.0.1:5000/pizza/submit_pizza/' + delivery_method,
                                                          order)

                        else:
                            # ask user if wanna edit more pizza?
                            cont = input("Edit more pizza? Y for Yes, other input for NO\n")
                            if cont != "Y":
                                # print(server_code.text)
                                break
            elif user_decision == "A":
                # user want to add a pizza to list
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
                        cur_topping = input(
                            "please Select pizza topping\n1: olives\n2: tomatoes\n3: mushrooms\n4: jalapenos\n5: "
                            "chicken\n6: "
                            "beef\n7: pepperoni\n")
                        cur_topping = switcher.pizza_topping_option(cur_topping)
                        if cur_topping == "Invalid OP":
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
                            "Id": user_order,
                            "Size": pizza_size,
                            "Type": pizza_type,
                            "Toppings": pizza_topping
                        }

                        pizza_json = json.dumps(order)
                        server_code = connection.post('http://127.0.0.1:5000/pizza/submit_pizza/' + delivery_method,
                                                      pizza_json)

                        if server_code.status_code == 404:
                            print("smothing wrong with you pizza, please enter the pizza again")
                        else:
                            print(server_code.text)
                            cont = input("add more pizza? Y for Yes, other input for NO\n")
                            if cont != "Y":
                                break
                    else:
                        new_list = ','.join(pizza_topping)
                        order = "Id,Size,Type,Toppings\n" + user_order + "," + pizza_size + "," + pizza_type + ",[" + str(
                            new_list) + "]"
                        server_code = connection.post('http://127.0.0.1:5000/pizza/submit_pizza/' + delivery_method,
                                                      order)
                        if server_code.status_code == 404:
                            print("smothing wrong with you pizza, please enter the pizza again")
                        else:
                            print(server_code.text)
                            cont = input("add more pizza? Y for Yes, other input for NO\n")
                            if cont != "Y":
                                break
            elif user_decision == "D":
                # user wants to delete pizza
                # all we need to do is to get the pizza
                # ask user which pizza you wanna change
                change_input = input("which pizza do you wanna Delete? enter pizza number, S for skip this session\n")

                if change_input == "S":
                    # no change any more for this session
                    break
                else:
                    # pop the target pizza
                    # try to get the target pizza
                    change_input = int(change_input) - 1
                    target_pizza = connection.get(
                        'http://127.0.0.1:5000/pizza/pop_single_pizza/' + user_order + "/" + str(change_input), "")
                    if target_pizza.text != "Order Id does not exist" or target_pizza.text != "Index is not valid":

                        print(target_pizza.text + " Delete Done")
                    else:
                        print(target_pizza.text)
            else:
                break
        # ask user if they want change drinks?
        drinks_list = connection.get("http://127.0.0.1:5000/pizza/get_drink_list/" + user_order, "")
        print(drinks_list.text)
        user_decision = input("do you want edit your drink? A for add, D for delete, other for skip")
        if user_decision == "A":
            # now ask for drink
            cur_drink = "Invalid OP"
            drinks = []
            while cur_drink == "Invalid OP":
                cur_drink = input("please Select drink to add \n1: Coke\n2: Diet Coke\n3: Coke_Zero\n4: Pepsi\n5: "
                                  "Diet_Pepsi\n6: "
                                  "Dr.Pepper\n7: Water\n8: Juice\n")
                cur_drink = switcher.drink_option(cur_drink)
                if cur_drink == "Invalid OP":
                    print("invalid input please try again\n")
                else:
                    drinks.append(cur_drink)
                    cur_drink = "Invalid OP"
                    cont = input("add one more drink? Y for Yes, other input for NO\n")
                    if cont != "Y":
                        break
            # now we have a pizza trying to send this pizza to the api and store it
            if delivery_method != "Foodora":
                order = {
                    "Id": user_order,
                    "Drink": drinks,
                }

                pizza_json = json.dumps(order)
                print(pizza_json)
                server_code = connection.post('http://127.0.0.1:5000/pizza/submit_drinks/' + delivery_method,
                                              pizza_json)

                if server_code.status_code == 404:
                    print("smothing wrong with you drink, please enter the drink again")
                else:
                    print(server_code.text)

            else:
                new_list = ','.join(drinks)
                order = "Id,Drink\n" + user_order + ",[" + str(new_list) + "]"
                print(order)
                server_code = connection.post('http://127.0.0.1:5000/pizza/submit_drinks/' + delivery_method, order)
                if server_code.status_code == 404:
                    print("smothing wrong with you drink, please enter the drink again")
                else:
                    print(server_code.text)
        elif user_decision == "D":
            while True:
                drinks_list = connection.get("http://127.0.0.1:5000/pizza/get_drink_list/" + user_order, "")
                print(drinks_list.text)
                # ask which drink they wanna remove
                delete_number = input("which drink do you want delete? left hands start at 1：\n")
                delete_number = int(delete_number) - 1
                server_code = connection.delete(
                    'http://127.0.0.1:5000/pizza/delete_drink/' + user_order + "/" + str(delete_number), "")
                print(server_code.text)

                # ask if user wanna delete more
                delete_more = input("do you want delete more? Y for yes other for No")
                if delete_more != "Y":
                    break
    else:
        print(server_code.text)

    return None
