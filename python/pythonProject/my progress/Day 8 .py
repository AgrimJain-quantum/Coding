dictionay = { 
    "name": "agrim",
    "age": 20
}
print(dictionay["name"])
print(dictionay["age"])
this_list = dict( name = "agrim" , age = 20, country = "india")
print(this_list)

car = {
"brand": "Ford",
"model": "Mustang",
"year": 1964
}
x = car.keys()
print(x) #before the change
car["color"] = "white"
print(x) #after the change

y = car.keys()
print(y) #after the change
z = car.values()
print(z) #after the change