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
def func():
    global x
    x = 20
func()
print(x)