x = 2
def value_x():
    x = 3
    print(f"x inside function: {x}")

value_x()
print(f"x outside function: {x}")


var1 = 5# var1 is in the global namespace 
def some_func(): # var2 is in the local namespace 
    var2 = 6
    def some_inner_func():  # var3 is in the nested local namespace
      var3 = 7