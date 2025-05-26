#to do
# we are making a coffe machine project 
# print a report of the resources in the machine
# check the sufficent resources
# process the money
# check the transaction successful
# return the change 
# make the coffee
MENU = {
    "espresso":{
        "ingredients": {
            "water" : 50,
            "coffee": 18,
        },
        "cost" : 5.0,
    },
    "latte" : {
        "ingredients": {
            "water" : 200,
            "milk" : 150,
            "coffee": 24,
        },
        "cost" : 10.0,           
    },
    "cappuccino" : {
        "ingredients": {
            "water" : 250,
            "milk" : 100,
            "coffee": 24,
        },
        "cost" : 15.0,           
    },
}
profit = 0.0
resources = {
    "water": 300,
    "milk": 300,
    "coffee": 300,
}



def is_resource_sufficient(ordered_ingredients):
    is_enough = True
    for item in ordered_ingredients: 
        if ordered_ingredients[item] >= resources[item]:
            print(f"Sorry there is not enough {item}.")
            is_enough = False
    return is_enough

def process_money():
    print("Please insert money.")
    total = 0.0
    ones = int(input("how many 1-ruppee coins? : "))
    total += ones * 1.0
    twos = int(input("how many 2-ruppee coins? : "))
    total += twos * 2.0
    fives = int(input("how many 5-ruppee coins? : "))
    total += fives * 5.0    
    tens = int(input("how many 10-ruppee coins? : "))
    total += tens * 10.0
    twenties = int(input("how many 20-ruppee coins? : "))
    total += twenties * 20.0
    return total
        
def is_transaction_successful(money_recevied, drink_cost):
    if money_recevied >= drink_cost:
        change = round(money_recevied - drink_cost, 2)
        print(f"Here is ${change} in change.")
        global profit
        profit += drink_cost
        return True
    else:
        print("Sorry that's not enough money. Money refunded.")
        return False

def make_coffee(drink_name, ordered_ingredients):
    """detuct the ingreedinetds from the resources"""
    for item in ordered_ingredients:
        resources[item] -= ordered_ingredients[item]
    print(f"Here is your {drink_name} ☕️. Enjoy!")


is_on = True
while is_on:
    choice = input("What would you like to have? (espresso/latte/cappuccino): ")
    if choice == "off":
        print("Turning off the machine.")
        is_on = False
    elif choice == "report":
        print(f"water : {resources['water']}ml")
        print(f"milk : {resources['milk']}ml")       
        print(f"coffee : {resources['coffee']}g" )
        print(f"profit : ${profit}")
    else:
        drink = MENU[choice]
        if is_resource_sufficient(drink["ingredients"]):
            payment = process_money()
            if is_transaction_successful( payment, drink["cost"]):
                make_coffee(choice, drink["ingredients"])




class CoffeeMachine:
    def init(self):
        self.resources = {
            "water" : 300,
            "milk" : 300,
            "coffee": 300
        }
    def report(self):
        print(f"water : {self.resources['water']}ml")
        print(f"milk : {self.resources['milk']}ml")       
        print(f"coffee : {self.resources['coffee']}g" )
        print(f"profit : ${profit}")
    def is_resource_sufficient(self, ordered_ingredients):
        is_enough = True
        