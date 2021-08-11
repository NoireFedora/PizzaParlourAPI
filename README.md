# Note
This Python API is fully developed me and my partner @zhuruisy to fullfill the requirement of CSC301 Assignment 2 that to create an API for a virtual pizza parlour, based on
some client requirements.

# A2-starter

Run the main Flask module by running `python3 PizzaParlour.py`

Run the main client by running `python3 main.py`

Run unit tests with coverage by running `pytest --cov-report term --cov=. tests/unit_tests.py`

## User Instructions
This is the instruction of how to use our program: <br>

Main Menu is located in the main.py file after running the main.py you will be asked which app to use, this include 
Uber, Foodora, In House Delivery and In Store Pickup From Store. Note option except In Store Pickup will require user 
input their address. <br>

After input the address user will have the following options to choose, note here if the user is entering the wrong 
option, the program will tell the user that the input is invalid and ask the user to input again. <br>

1: Create order <br>
2: Edit order <br>
3: Cancel order <br>
4: Submit order <br>
5: Menu <br>
6: Add pizza type <br>
7: Back

#### 1. Create order
To create an order, the program will require a new order id from the backend and ask the user to select size, topping 
and pizza type. note here since some of the pizza type can be added later by the user so only the pizza type is not in 
the fixed option. The user can only select one type and one size but multiple topping by input Y after each topping 
selection. After finishing select pizza, if the pizza type is not valid the api will send a warning and that pizza 
will not be stored. the user can add another pizza by selecting Y after the submission. <br>

After adding all the pizza, the user will be asked to add a drink and the user can add multiple drinks by entering Y 
after selecting the drinks. <br>

After finishing select the drink program will send the drink order to the api and print that order created and also 
returns the order ID for user later use.

#### 2. Edit order
The first user will be asked for the order id that they want to edit, if the order id does not exist the program will 
return an error message and return to the last menu. <br>

Then the program will ask user if they want to Edit pizza include add delete or edit existing pizza if you choose add 
pizza user will be directed to a process that create a new pizza like the one in create order, if user choose Delete 
then the program will ask which pizza number user wants to delete and if the pizza number exist program will remove 
that pizza by pop that pizza and not return back, and also print pizza message and delete success. otherwise the 
program will return an error message and go back to the last menu. <br>

If Edit is selected, the program will ask the user if they want to change the topping type or size. user can choose 
skip or change, if user choose change the program will ask the user to enter a new set of topping, size or type 
depending on which one user choose to edit. After done the program will add the pizza back(may not have the same pizza 
number) in case the new type is not valid or something went wrong the old pizza will be sent back to the api which 
keeps the order unchanged. <br>

After edit the pizza program will ask the user if they want to use edit drink include add drink or Delete drink. 
If users choose to add they will be asked to create a list of drinks and the program will add this drink to the 
original drinklist. If the user chooses delete, the program will ask usr which drink to delete and delete the target 
drink if the drink exists otherwise it will print an error message. This delete process can be repeated by keeping Y.


#### 3. Cancel order
The Program will ask users to provide and if the order exists program will send order id to api and delete the target 
order otherwise program will display error message and return to last level.

#### 4. Submit order
Similar to cancel order the user will provide the order id and the program will display the information of the order 
and symbolize that the order is submitted. Please note that the order will not be deleted after this as users can edit 
this order and resubmit later. program will display an error message and jump to the last menu if the order number is 
invalid.

#### 5. Menu
There are two options: one is to search the target item and another is to require the entire menu. If the user chooses 
to search, the program will ask the user to provide an item name and if the name exists the program will return the 
price otherwise the program will return an error message and go back. If the user chooses the entire message the 
program will display the entire menu.

#### 6. Add Pizza Type
Program will ask user to enter pizza type and pizza price and as long as the price is in digit the program will add 
it to the menu.

## Pair Programming:
In general, our program is divided into two parts: **API** part and **Client** Part, and each person is responsible for 
one part (Yicheng Xue for API and Rui Zhu for Client). Rui looked for which API function and then Yicheng wrote it.
We did pair programming on some features through screen sharing on discord and will show them as following:<br>

(We **apologize** for we forget we have to show drivers for each feature on commit. Therefore, the commit is messed up 
and will not reflect our pair programming but we actually did it.)

#### 1. Submit a Pizza - API
Driver: Rui Zhu <br>
Navigator: Yicheng Xue <br>

Since Rui has experience of writing API, he wrote this feature as a reference to teach Yicheng with explanation. 
It was very easy to understand through pair programming and was a very good start to writing API parts. Originally, we 
planned to submit everything together in the client (this is why you can find a commit implementing “Submit New Order” 
at the very beginning) but we found it did not work well, so we split everything after. After Rui finished it, he used 
Postman to test it and taught Yicheng how to use Postman to test API. After we decided to use Factory Design Pattern, 
Yicheng improved this feature with the use of Object. In general, pair programming helps Rui teach Yicheng how to write 
API and help us find the design problems immediately, which is the positive part of this process.

#### 2. Submit Drinks - API
Driver: Yicheng Xue <br>
Navigator: Rui Zhu <br>

Yicheng wrote this as his first attempt at writing API and Rui helped him with any part he did not understand. Since 
it is similar to “Submit a Pizza”, it was very easy to complete it. After discussion, we decided to use the Factory 
Design Pattern that makes Pizza and Order as Object and let Order Object to store all Pizza and Drinks in one Order. 
After that, Yicheng improved this feature with the implementation of the design pattern and the test of Postman. In 
general, pair programming helps Yicheng to learn to write API with Rui’s navigation and can let us discuss immediately 
when we find problems during coding, which is the positive part of this process.

#### 3. Check Order - API
Driver: Yicheng Xue <br>
Navigator: Rui Zhu <br>

Since our structure makes every user input upload to the server and is able to submit the whole order only if the order 
has all necessary information, we need to write this function to check the validity of target order when users want to 
submit. Since Rui wants to directly print the return result to the client, Yicheng follows Rui’s requirement and 
instruction to return a receipt string. However, Yicheng thought returning a file should be better than returning a 
string to the client since he thought this task should be done by the client. Rui explained that his client only needs 
a string and transferring data to string is easier to do in server not in client since we use Object to store data. 
After Yicheng finished it based on Rui’s preference, we directly tested this feature on Rui’s client and saw the result 
together. In general, pair programming can let us discuss immediately when we find problems during coding. However, 
sometimes the style and preference of people writing code is different and both opinions are correct. It was hard to 
make a decision on both two correct options.

#### 4. Edit Order - Client
Driver: Rui Zhu <br>
Navigator: Yicheng Xue <br>

This part of the CLI needs a lot of interaction with API thus we have Yichen doing the Navigator job. The main working 
process is that when Rui is writing a feature that needs support from API Yicheng will give the specific input that 
needed for the assignment and output that API will return. We find this method of working is very useful as it saves 
the time for the programmer to read through the API implementation and having a person who can talk about the 
implementation can help understand the scope of the entire API. <br>

We also use the prototype design pattern in the Edit order part that we first get the pizza from API and we have made 
a copy of that pizza so if some part is not changed we can use the original part of the pizza to fill that. Also in 
case if the new pizza is invalid we can put the original one back.

## Program Design

#### Design Pattern
The first design pattern we are using is **Factory** pattern, as each time API need a pizza object from CLI in different 
form depends on the delivery app or if it is drink(a different version of Pizza) although in this assignment we don’t 
have a specific function to do the factory job, but we have a clear pattern that accept different information and made 
them into different json or csv format.

#### Relationships between objects
We have two Objects: **Pizza** and **Order**. Both of them have no function method since we think python is unlike Java that 
has private and public attributes so some get/edit methods are not necessary. We only use these Objects to save 
information with a format. There is a global dictionary “orders” stores all Order Objects with their 
unique “order_id”(an attribute of Order) as key (Example: {“1”: Order Object with order_id 1}). Order has an attribute 
called “pizza_list” which has a list that stores all Pizza Objects with the same order_id as this Order 
(Example: Order.pizza_list = [Pizza 1, Pizza 2, Pizza 3]). 

#### Function Design
**API Part**
* **Submission**(submit_pizza, submi_drinks, submit_address):<br>
We will record temporary Order in our server so every time the user input legal information the server will record it. 
We separate the submission of these three types of information so that we don't have to submit a whole Order when the 
user input something. For the submission of Pizza, we found that directly submitting a complete Pizza(with all required 
attributes) is better than submitting a size/type/topping of a Pizza to change a specific element 
(same effect but with less code and simpler logic).

* **Delete**(pop_single_pizza, delete_drink, cancel_order): <br>
Since we will submit a complete Pizza, the client needs all information of the target Pizza. After the user edited the 
Pizza, the client used the input and provided information from the server to make a new Pizza as a file and then use 
submit_pizza to submit. Therefore, we used the pop method for both editing and deleting Pizza.

* **Get**(get_pizza_list, get_drink_list, get_menu): <br>
Simply show the user in the client the information they want.

* **Submit an order**(check_order): <br>
Check the Order has all required information (validity has been checked during submission) then make Order.submitted = 
true and return the string of receipt to the client. Since we are not required to write additional functions after 
submitting an Order (like an Order is complete, communicating with drivers, making a review on an Order, etc), 
this attribute is not used in any functions and just shows our idea and logic here. If Order.submitted == false, 
it is a temporary order. In other words, we stored the temporary Order directly in the server rather than saved 
in a temporary file. In addition, Order has an attribute “total” that calculates the order dynamically 
during submission/editing/deleting, as the requirement. 

* **Add/Edit something in the menu**(add_menu): <br>
Since we totally have no idea of why the customer is able to change the menu, we just create a simple function that can 
add and edit something in the menu with given name and price. Delete something in the menu will influence the result of 
unit tests since we read menu.json in many unit tests and validity checks will be influenced a lot, so we didn't write 
it.

**Client Part**
* **main.py**
The main page of the program, call create_order() submit_order() cancel_order() pull_menu() edit_order() 
add_Pizza_type() depends on user input.

* **switch.py**
Contains the switch helper function for the program, it mainly used in format user input into a more detailed text 
and easy for understanding.

* **connection.py**
Contains helper functions that handle the interaction with the APIs. It also helps when debugging and handles the error.

* **create_order() submit_order() cancel_order() pull_menu() edit_order() add_Pizza_type()**:
These functions are main logic functions <br>

**create_order()** <br>
Get user input and create pizza and/or drink objects and send them to API as json or CSV. One thing 
to be noticed is that due to simplifying the process of the backend we choose not to send an entire order at once but 
to send each pizza at a time. This also provides a positive side is that during update/edit pizza we can use the same 
process on edit them.

**submit_order() cancel_order()** <br>
Both of them get the order ID from the user and send it to API to get the result.
 
**edit_order()** <br>
Instead of letting the user decide which thing to change, we will ask the user of each item and let the user decide 
which item to change. Delete pizza is using pop api and not add anything back and edit is add the modified pizza back. 
Add pizza and add drink will simply use the same process in the create order and send them into API.

**pull_menu()** <br>
This function receives either user input and depends on the input print the entire menu or specific item.

**add_Pizza_type()** <br>
Get the type name and the price from the user and send them to API and save.

## Code Craftsmanship
Both Yicheng and Rui used PyCharm IDE to create clean code.

## Other
During test we find out that 100% of the function are having api calls which we have not find a way to mock those API 
returns (prof answer the piazza in friday morning but we do not have enough time) so we can only cover 5% of the 
operation.py and 30% of the main function as we can only test those input fail case that do not require API call.
By the way, our unit tests of testing API (PizzaParlour.py) has 91% line coverage.
