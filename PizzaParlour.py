from flask import Flask, request

app = Flask("Assignment 2")

@app.route('/pizza')
def welcome_pizza():
    return 'Welcome to Pizza Planet!'

# first we need a library
orders = {}

@app.route('/pizza/submut_order', methods = ['POST'])
def submit_order():
    content = request.get_json()
    print(content['Pizza']['Size'])
    return content

@app.route('/pizza/update_order/<orderid>', methods = ['POST'])
def update_order(orderid):
    print(orderid)
    return "update done"

if __name__ == "__main__":
    app.run()
