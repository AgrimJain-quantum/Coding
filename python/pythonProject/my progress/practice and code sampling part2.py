def my_function():
    print("Hello from a function")
my_function()

def my_function_with_args(username, greeting):
    print(f"Hello, {username}, from a function! I wish you {greeting}")
my_function_with_args("John Doe", "a great day!")

def sum_two_numbers(a, b):
    return a + b
print(sum_two_numbers(5, 7))

def print_sum_two_numbers(a, b):
    print(a + b)
print_sum_two_numbers(5, 7)

def print_sum_two_numbers(a, b):
    print(a + b)
    return a + b
print(print_sum_two_numbers(5, 7))

