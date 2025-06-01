from turtle import Turtle, Screen
tim = Turtle()
screen = Screen()
    
def move_forwards():
    tim.forward(10)
    










screen.listen()
screen.onkey(key = "space" , fun = move_forwards)
screen.exitonclick()










































# def add(n1, n2):
#     return n1 + n2
# def subtract(n1, n2):
#     return n1 - n2
# def multiply(n1, n2):
#     return n1 * n2
# def divide(n1, n2):
#     return n1 / n2
# '''this is a higher order function'''
# def calculate(n1, n2, operation):
#     return operation(n1, n2)
# result = calculate(10, 5, add)
# print(result)  # Output: 15
# result1 = calculate(10, 5, subtract)
# print(result1)  # Output: 5
# result2 = calculate(10, 5, multiply)
# print(result2)  # Output: 50
# result3 = calculate(10, 5, divide)
# print(result3)  # Output: 2.0
