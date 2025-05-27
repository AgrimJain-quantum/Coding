# import turtle
# timmy = turtle.Turtle()
# def draw_square(size):
#     for _ in range(4):
#         timmy.forward(size)
#         timmy.right(90)

# def draw_dashed_line(length, dash_length):
#     for _ in range(length // (2 * dash_length)):
#         timmy.forward(dash_length)
#         timmy.penup()
#         timmy.forward(dash_length)
#         timmy.pendown()

# from turtle import Turtle , Screen
# my_screen = Screen()
# timmy = Turtle()
# print(my_screen.canvheight)
# timmy.shape("turtle")
# timmy.color("DarkMagenta")
# timmy.forward(100)
# print(timmy)
# my_screen.exitonclick()

# def __init__(self, x, y):
#     self.x = x
#     self.y = y
# def __str__(self):
#     return f"Point({self.x}, {self.y})"
# class Dog:
#     species = "Canine"  # Class attribute

#     def __init__(self, name, age, breed):
#         self.name = name  # Instance attribute
#         self.age = age  
#         self.breed = breed 

# # Creating an object of the Dog class
# dog1 = Dog("Buddy", 3, "Golden Retriever")

# print(dog1.name)  # Output: Buddy
# print(dog1.species)  # Output: Canine
# print(dog1.age)  # Output: 3
# print(dog1.breed)

class Person:
    def __init__(self , name, age, weight, height):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height
        
    def greet(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")
    
person1 = Person("Alice", 30, 65, 170)
person1.greet()  # Output: Hello, my name is Alice and I am 30 years old.

class Dog:
    sound = "Woof"
dog1 = Dog()
print(dog1.sound)
