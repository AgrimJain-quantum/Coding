# dictionay = { 
#     "name": "agrim",
#     "age": 20
# }
# print(dictionay["name"])
# print(dictionay["age"])
# this_list = dict( name = "agrim" , age = 20, country = "india")
# print(this_list)

car = {
"brand": "Ford",
"model": "Mustang",
"year": 1964
}
# x = car.keys()
# print(x) #before the change
# car["color"] = "white"
# print(x) #after the change

# y = car.keys()
# print(y) #after the change
# z = car.values()
# print(z) #after the change
# s = car.items()
# print(s) #after the change

# travel_log = {
#     "france" : [
#         {
#             "cities_visited" : ["paris", "lille", "lyon"],
#             "total_visits" : 12
#         },
#         {
#             "cities_visited" : ["paris", "lille", "lyon"],
#             "total_visits" : 12
#         }
#     ]
# }
# print(travel_log["france"][0]["cities_visited"])

nested_list = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(nested_list[1])  # Output: 2
print(nested_list[0][2])  # Output: 6
car["year"] = 2020
print(car)
car.update({"model" : "maruti"})
print(car)

nested_list_dictionary = {
    "list1" : [1, 3, 4],
    "list2" : { "list3" : [1, 2, 3], "list4" : [4, 5, 6] }
}
print(nested_list_dictionary["list2"]["list4"][1])  # Output: 5
print(nested_list_dictionary["list1"][2])
car.update({"model" : "porshe"})
print(car)  # Output: None
car.update({"year" : 2025})
print(car)  # Output: None
