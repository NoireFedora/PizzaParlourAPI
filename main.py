import switcher
import operations

Address = ""


def main():
    global Address
    while True:
        print("***************Welcome to Pizza parlour***************\n How do you wanna get your food today?")
        # ask user what do they want
        delivery_method = "Invalid code"
        while delivery_method == "Invalid code":
            op_code = input("1: Uber\n2: Foodora\n3: Pizza parlour Agent\n4: In-store\n5: exit\n")
            delivery_method = switcher.delivery_option(op_code)

            if delivery_method == "Invalid code":
                print("input is not valid please try again\n")
        if delivery_method == "Q":
            break
        while Address == "":
            if delivery_method != "Instore":
                Address = input("please enter you address\n")
        # ask what does user wanna do

        while True:
            operation_input = input("What do you wanna do Today?\n1: create order\n2: edit order\n3: cancel order\n4: "
                                    "submit order\n5: menu\n6: Back\n")
            operation = switcher.operation_option(operation_input)
            if operation == "Invalid OP":
                print("sorry you operation is invalid please reselect")
            elif operation == "create":
                # creat order
                code = operations.creat_order(delivery_method, Address)
            elif operation == "Q":
                break

    print("thank you for visiting Pizza parlour today\n")


if __name__ == "__main__":
    main()
