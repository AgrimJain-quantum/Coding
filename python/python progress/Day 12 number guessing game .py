# x = 2
# def value_x():
#     x = 3
#     print(f"x inside function: {x}")

# value_x()
# print(f"x outside function: {x}")


# var1 = 5# var1 is in the global namespace 
# def some_func(): # var2 is in the local namespace 
#     var2 = 6
#     def some_inner_func():  # var3 is in the nested local namespace
#       var3 = 7
    
# count = 5

# def some_method():
#     global count
#     count = count + 1
#     print(count)

# some_method()
# # Output: 6

# def some_func():
#     def some_inner_func():
#         var = 10
#         print("Inside inner function:", var)
#     some_inner_func()
# print("Outside inner function:", var)

# some_func()


# def outer_funtion():
#     def inner_funtion():
#         print("this is inner funtion")
#     inner_funtion()
# outer_funtion()

# def qw_1():
#     s = "hello"
#     print(s)
# s = "world"
# qw_1()
# print(s)

# count = 5
# def some_method():
#     global count
#     count = count + 1
#     print(count)

# def outer():
#     def inner():
#         var = 10
#         print(var)
#     inner()
#     print(var)

# count = 5
# def some_method():
#     global count
#     count = count + 1
#     print(count)
# some_method()



# def some_func():
#     def some_inner_func():
#         vars = 10
#         print("Inside inner function:", vars)
#     some_inner_func()
#     print("Outside inner function:", vars)
# some_func()

# count = 5
# def some_method():
#     global count
#     count = count + 1
#     print(count)
# some_method()



# '''python local variable'''
# def f():
#     s = "hello"
#     print(s)
# f()

# '''python global variable'''
# q = "agrim"
# def qw():
#     print(q)
# qw()

# ''' python nopnlocal variable'''
# def outer():
#     x = "local"
#     def inner():
#         nonlocal x
#         x = "nonlocal"
#         print("inner:", x)
#     inner()
#     print("outer:", x)


#     # global scope
# player_health = 10
# def drink_potion():
#     potion_strength = 2
#     print(player_health)
# drink_potion()

# level = 3
# enemies = ["skeleton", "zombie", "mummy"]

# def create_enemy():
#     new_enemy = ""
#     if level < 5:
#         new_enemy = enemies[0]
#     print(new_enemy)

# x = 10 
# def func():
#     global x
#     x = 20
# func()
# print(x)


# """non local keyword"""
# def outer():
#     x = 10
#     def inner():
#         nonlocal x
#         x = 20
#         print("inner:" , x)
#     inner()
#     print("outer: ", x)
# outer()

# PI = 3.14
# GRAVITY = 9.8
# def calculate_area(radius):
#     return PI * radius * radius
# print(calculate_area(5))
# def something():
#     return PI * GRAVITY
# print(something())


# def a_function(a_parameter):
#     a_variable = 15
#     return a_parameter
 
# a_function(10)
# print(a_variable)


# i = 50
# def foo():
#     i = 100
#     return i
 
# foo()
# print(i)


# def bar():
#     my_variable = 9
 
#     if 16 > 9:
#       my_variable = 16
 
#     print(my_variable)
 
# bar()

""" guess the number game """

# todo
# choosing A random number between 1 and 100
# funtion to check the difficulty
# let the user guess the number 
# function to check the guess
# track the number of guesses and remaining attempts
# repeat the guessing functionality if they get it wrong
from random import randint



EASY_LEVEL_TURNS = 10
HARD_LEVEL_TURNS = 5


# Function to check users' guess against actual answer
def check_answer(user_guess, actual_answer, turns):
    """Checks answer against guess, returns the number of turns remaining."""
    if user_guess > actual_answer:
        print("Too high.")
        return turns - 1
    elif user_guess < actual_answer:
        print("Too low.")
        return turns - 1
    else:
        print(f"You got it! The answer was {actual_answer}")


# Function to set difficulty
def set_difficulty():
    level = input("Choose a difficulty. Type 'easy' or 'hard': ")
    if level == "easy":
        return EASY_LEVEL_TURNS
    else:
        return HARD_LEVEL_TURNS


def game():
    
    # Choosing a random number between 1 and 100.
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    answer = randint(1, 100)
    print(f"Pssst, the correct answer is {answer}")

    turns = set_difficulty()

    # Repeat the guessing functionality if they get it wrong.
    guess = 0
    while guess != answer:
        print(f"You have {turns} attempts remaining to guess the number.")
        # Let the user guess a number
        guess = int(input("Make a guess: "))
        # Track the number of turns and reduce by 1 if they get it wrong
        turns = check_answer(guess, answer, turns)
        if turns == 0:
            print("You've run out of guesses, you lose.")
            return
        elif guess != answer:
            print("Guess again.")




game()


