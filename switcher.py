# switcher function
def delivery_option(code):
    switcher = {
        "1": "Uber",
        "2": "Foodora",
        "3": "PizzaP",
        "4": "Instore",
        "5": "Q"
    }
    return switcher.get(code, "Invalid code")


def operation_option(code):
    switcher = {
        "1": "create",
        "2": "edit",
        "3": "cancel",
        "4": "submit",
        "5": "menu",
        "6": "Q"
    }
    return switcher.get(code, "Invalid OP")


def pizza_size_option(code):
    switcher = {
        "1": "Small",
        "2": "Medium",
        "3": "Large",
        "4": "Extra_large"
    }
    return switcher.get(code, "Invalid OP")


def pizza_topping_option(code):
    switcher = {
        "1": "Olives",
        "2": "Tomatoes",
        "3": "Mushrooms",
        "4": "Jalapenos",
        "5": "Chicken",
        "6": "Beef",
        "7": "Pepperoni"
    }
    return switcher.get(code, "Invalid OP")
