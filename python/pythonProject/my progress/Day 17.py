# class User:
#     pass
# user_1 = User()
# # class creation
# class Dog:
#     species = "c"
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age  
# # object creation
# dog1 = Dog("buddy" , 3)
# print(dog1.name)
# print(dog1.age)
# dog1.name = "max"
# print(dog1.name)  # Output: max
# dog1.age = 4
# print(dog1.age)  # Output: 4
# dog2 = Dog("Charlie", 5)
# print(dog2.name)  # Output: Charlie
# print(dog2.age)  # Output: 5

import prettytable
class Person:
    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight
name1 = Person("Alice", 30, 65)
name2 = Person("Bob", 25, 70)
table = prettytable.PrettyTable()
table.field_names = ["Name", "Age", "Weight"]   
table.add_row([name1.name, name1.age, name1.weight])
table.add_row([name2.name, name2.age, name2.weight])
print(table)

class user:
    pass

user_1 = user()
user_1.name = "agrim"
user_1.age = 20
user_1.weight = 70
user_2 = user()
user_2.name = "jain"
user_2.age = 21
user_2.weight = 75
print(user_1.name)  # Output: agrim``

# def function():
#     pass

# print("hello")
# user_1.funtion = function

# AgrimJain = pascal case
# agrim_jain = snake case
# agrimJain = camel case
# class car:
#     def __init__(self, model, color, year):
#         self.model = model
#         self.color = color
#         self.year = year
#     def start(self):
#         print(f"The {self.color} {self.model} is starting.")
#     def stop(self):
#         print(f"The {self.color} {self.model} is stopping.")
# car1 = car("Toyota", "red", 2020)
# car2 = car("Honda", "blue", 2021)
# car1.start()  # Output: The red Toyota is starting.
# car2.stop()   # Output: The blue Honda is stopping.
