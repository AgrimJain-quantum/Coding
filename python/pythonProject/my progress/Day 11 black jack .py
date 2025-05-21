''' doc string - triple quoted string
'''
def fun3(a,b):
    c = a / b
    return c
print(fun3(2,3))

def my_function():
    '''Demonstrates triple double quotes
    docstrings and does nothing really.'''
 
    return None

print("Using __doc__:")
print(my_function.__doc__)

print("Using help:")
help(my_function)

