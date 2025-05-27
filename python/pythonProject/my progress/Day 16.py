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
class Dog:
    species = "Canine"  # Class attribute

    def __init__(self, name, age):
        self.name = name  # Instance attribute
        self.age = age  # Instance attribute

# Creating an object of the Dog class
dog1 = Dog("Buddy", 3)

print(dog1.name)  # Output: Buddy
print(dog1.species)  # Output: Canine