# print(type("Hello"))
# print(type(1))
# print(type(1.0))
# print(type(True))
# print(type([1, 2, 3]))
# print(type((1, 2, 3)))
# print(type({"name": "John", "age": 23}))
# print(type({1, 2, 3}))
# print(type(None))
# print(type(type))
# print(type(print))
# print(type(len))
# print(type(type(1)))
# int("123")
# print(int("123"))   
# print(int(123.45))
# print(int("123.45"))
print("Number of letters in your name: " + str(len(input("What is your name? "))))
# Integer to float
# x = 5    # int
# y = 2.0  # float
# z = x + y  # Python implicitly converts x to float
# print(z, type(z))  # Output: 7.0 <class 'float'>
# print("x+y = " + str(z))
# # Float to integer
# x = 5.0    # float
# y = 2.0    # float
# z = x + y  # Python implicitly converts x and y to float
# print(z, type(z))  # Output: 7.0 <class 'float'>
# print("x+y = " + str(z))

num_str = "42"
num_int = int(num_str)
print(num_int, type(num_int))  # Output: 42 <class 'int'>

num = 5
num_float = float(num)
print(num_float, type(num_float))  # Output: 5.0 <class 'float'>

num = 10
num_str = str(num)
print(num_str, type(num_str))  # Output: "10" <class 'str'>
