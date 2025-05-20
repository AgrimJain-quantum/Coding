# thisdict = {
#     "brand" : "aston martin",
#     "model" : "db11",
#     "year" : 2020,
# }
# thisdict.pop("model")
# print(thisdict)
# thisdict.popitem()
# print(thisdict)
# del(thisdict["brand"])
# print(thisdict)
# this = {
#     "brand" : "aston martin",
#     "model" : "db11",
#     "year" : 2020,
#     "color" : "red",
#     "engine" : "v8",
#     "horsepower" : 503,
#     "torque" : 498,
#     "weight" : 3855,
#     "top_speed" : 208,
# }
# this.copy()
# thisdict = {
#     "brand" : "aston martin",
#     "model" : "db11",
#     "year" : 2020,
# }
# thisdict.clear()
# print(thisdict)
# this.items()
# print(this)
# this.fromkeys(thisdict)
# print(this)
# car = {
#     "brand" : "aston martin",
#     "model" : "db11",
#     "year" : 2020,
#     "color" : "red",
# }
# mydict = car.copy()
# print(mydict)
# qwerty = {
#     "brand" : "aston martin",
#     "model" : "db11",
#     "year" : 2020,
#     "color" : "red",
#     "engine" : ["v8", "v12"],
#     "horsepower" : 503,
#     "weight" : 3855,
#     "top_speed" : 208,
#     "acceleration" : 0.0,
#     "braking" : 0.0,
#     "handling" : 0.0,
#     "comfort" : 0.0,
# }
# qwerty.fromkeys("engine")
# print(qwerty)
# returnq = {
#     "name" : "agrim ",
#     "second_name" : "jain",
#     "age" : 20,
# }
# returnq.popitem()
# print(returnq)  
# returnq.pop("name")
# print(returnq)
# \
# def my_function():
#     return 3 * 2
# print(my_function())

# my_list = [1,2,3,4,5]
# my_list.pop(2)
# print(my_list)
# my_list.pop(0)
# print(my_list)
# my_list.pop
# print(my_list)

# print(my_list[-1])

# list = ["agrim" , "jain" , "20" , "28 ", "june" , "2005"]
# print(list[2:6]     )
# def my_function(f_name , last_name):
#     name_1 = f_name.title()
#     name_2 = last_name.title()
#     return f"hello {name_1} {name_2}"
# print(my_function("agrim" , "jain"))
def function_1(text):
    return text + text
def function_2(text):
    return text.title()
output  = function_2(function_1("agrim"))
print(output)


