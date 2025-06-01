# import turtle as t
# import random

# tim = t.Turtle()

# ########### Challenge 3 - Draw Shapes ########

# colours = ["CornflowerBlue", "DarkOrchid", "IndianRed", "DeepSkyBlue", "LightSeaGreen", "wheat", "SlateGray", "SeaGreen"]

# def draw_shape(num_sides):
#     angle = 360 / num_sides
#     for _ in range(num_sides):
#         tim.forward(100)
#         tim.right(angle)

# for shape_side_n in range(3, 10):
#     tim.color(random.choice(colours))
#     draw_shape(shape_side_n)



# import turtle as t
# import random
# tim = t.Turtle()
# #Challenge 1 - draw a square
# tim.fd(100)
# tim.right(90)
# tim.fd(100)
# tim.right(90)
# tim.fd(100)
# tim.right(90)
# tim.fd(100)
# #Challenge 2 - draw a dashed line
# for _ in range(15):
#     tim.fd(10)
#     tim.penup()
#     tim.fd(10)
#     tim.pendown()
# #Challenge 3 - draw shapes
# colours = ["CornflowerBlue", "DarkOrchid", "IndianRed", "DeepSkyBlue", "LightSeaGreen", "wheat", "SlateGray", "SeaGreen"]
# def draw_shape(num_sides):
#     angle = 360 / num_sides
#     for _ in range(num_sides):
#         tim.forward(100)
#         tim.right(angle)
# for shape_side_n in range(3, 10):
#     tim.color(random.choice(colours))
#     draw_shape(shape_side_n)
# screen = t.Screen()
# screen.exitonclick()
# timm = t.Turtle()
# t.colormode(255) 

# def random_color():
#     r = random.randint(0, 255)
#     g = random.randint(0, 255)
#     b = random.randint(0, 255)
#     random_color = (r, g, b)
#     return random_color


# directions = [0, 90, 180, 270]
# timm.pensize(15)
# timm.speed("fastest")
# for _ in range(1000):

#     timm.color(random_color())
#     timm.forward(30)
#     timm.setheading(random.choice(directions))

# # challenge 5 - Spirograph
# import turtle as t
# import random

# tim = t.Turtle()
# t.colormode(255)
# def random_color():
#     r = random.randint(0, 255)
#     g = random.randint(0, 255)
#     b = random.randint(0, 255)
#     color = (r, g, b)
#     return color

# ########### Challenge 5 - Spirograph ########
# tim.speed("fastest")
# def draw_spirograph(size_of_gap):
#     for _ in range(int(360 / size_of_gap)):
#         tim.color(random_color())
#         tim.circle(100)
#         tim.setheading(tim.heading() + size_of_gap)

# draw_spirograph(5)
  
# #  hirst painting
# screen = t.Screen()
# screen.exitonclick()

import colorgram 

colorgram.extract('image.jpg', 30)