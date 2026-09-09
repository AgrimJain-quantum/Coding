# def my_function():
#     print("Hello from a function")
# my_function()

# def my_function_with_args(username, greeting):
#     print(f"Hello, {username}, from a function! I wish you {greeting}")
# my_function_with_args("John Doe", "a great day!")

# def sum_two_numbers(a, b):
#     return a + b
# print(sum_two_numbers(5, 7))

# def print_sum_two_numbers(a, b):
#     print(a + b)
# print_sum_two_numbers(5, 7)

# def print_sum_two_numbers(a, b):
#     print(a + b)
#     return a + b
# print(print_sum_two_numbers(5, 7))

# def print_sum_two_numbers(a, b):
#     return a + b
#     print(a + b)            
# print(print_sum_two_numbers(5, 7))

# def print_sum_two_numbers(a, b):
#     print(a + b)
#     return a + b
# print(print_sum_two_numbers(5, 7))


# for i in range(5):
#     print(i)
# else:
#     print("Loop completed")

# def factorial(n):
#     if n == 0 or n == 1:
#         return 1
#     return n * factorial(n - 1)

# print(factorial(5))  # Output: 120

# def my_fuction():
#     print("Hello from a function")
# my_fuction()

# def greet(name):
#     print(f"Hello, {name}!")  # Code block for the function
# greet("Agrim")

# def add(*args):
#     print(args[1])
#     sum = 0
#     for n in args:
#         sum += n
#     return sum
# print(add(1, 2, 3))

# def calculate(n, **kwargs):
#     print(kwargs)
#     # for key, value in kwargs.items():
#     #     print(f"{key} = {value}")
#     n += kwargs["add"]
#     n *= kwargs["multiply"]
#     print(n)
# calculate(2, add = 3, multiply = 5)  

# class Car:
#     def __init__(self,**kw):
#         self.make = kw["make"]
#         self.model = kw["model"]
#         self.color = kw["color"]
#         self.seats = kw["seats"]  # Default to 5 seats if not provided 
# my_car = Car(make="Nissan", model="GTR",  color="Red", seats=4)
# print(my_car.seats)

# def bar(spam, eggs, toast='yes please!', ham=0):
#     print(spam, eggs, toast, ham)
 
# bar(1, 2)

# def bar(spam, eggs, toast='yes please!', ham=0):
#     print(spam, eggs, toast, ham)
 
# bar(toast='nah', spam=4, eggs=2)

# def test(*args):
#     print(args)
 
# test(1,2,3,5)

# def test(*args):
#     print(args)
 
# test(1,2,3,5)

def all_aboard(a, *args, **kw): 
    print(a, args, kw)
 
all_aboard(4, 7, 3, 0, x=10, y=64)

