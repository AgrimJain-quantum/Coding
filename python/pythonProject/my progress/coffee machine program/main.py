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
