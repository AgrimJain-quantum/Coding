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



import turtle as t
import random
tim = t.Turtle()
#Challenge 1 - draw a square
tim.fd(100)
tim.right(90)
tim.fd(100)
tim.right(90)
tim.fd(100)
tim.right(90)
tim.fd(100)
#Challenge 2 - draw a dashed line
for _ in range(15):
    tim.fd(10)
    tim.penup()
    tim.fd(10)
    tim.pendown()
#Challenge 3 - draw shapes
colours = ["CornflowerBlue", "DarkOrchid", "IndianRed", "DeepSkyBlue", "LightSeaGreen", "wheat", "SlateGray", "SeaGreen"]
def draw_shape(num_sides):
    angle = 360 / num_sides
    for _ in range(num_sides):
        tim.forward(100)
        tim.right(angle)
for shape_side_n in range(3, 10):
    tim.color(random.choice(colours))
    draw_shape(shape_side_n)
screen = t.Screen()
screen.exitonclick()
