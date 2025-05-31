# # from turtle import Turtle, Screen
# # timmy_the_turtle = Turtle()
# # timmy_the_turtle.shape("turtle")
# # timmy_the_turtle.color("oliveDrab4")
# # timmy_the_turtle.forward(100)   
# # timmy_the_turtle.right(90)
# # timmy_the_turtle.forward(100)
# # timmy_the_turtle.right(90)
# # timmy_the_turtle.forward(100)
# # timmy_the_turtle.right(90)
# # timmy_the_turtle.forward(100)


# # screen = Screen()
# # screen.exitonclick()
# # from turtle import *
# # from random import *
# # tim = Turtle()
# # tom = Turtle()
# # terry = Turtle()
# # tim.shape("turtle")
# # tom.shape("turtle")
# # terry.shape("turtle")
# # tim.color("red")
# # tom.color("blue")
# # terry.color("green")
# # tim.forward(100)
# # tom.forward(100)
# # terry.forward(100)
# # screen = Screen()
# # screen.exitonclick()


# # def draw_square(turtle):
# #     for _ in range(4):
# #         turtle.forward(100)
# #         turtle.right(90)

# # import turtle as t
# # timmy = t.Turtle()
# # timmy.shape("turtle")
# # timmy.color("oliveDrab4")
# # for _ in range(36):
# #     draw_square(timmy)


# #     timmy.right(10)

# import heroes
# print(heroes.gen())

import turtle as t
tim = t.Turtle()
for _ in range(15):
    tim.forward(10)
    tim.penup()
    tim.forward(10)
    tim.pendown()

screen = t.Screen()
screen.exitonclick()
