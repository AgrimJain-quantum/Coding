# def format(f_name, l_name):
#  print(f_name.title())
#  print(l_name.title())
#  formatted_f_name  = f_name.title()
#  formattted_l_name = l_name.title()
#  print(f" hi! {formatted_f_name} {formattted_l_name}")
# print(format("agrim", "jain"))


def format_name(f_name, l_name):
 if f_name == "" or l_name == "":
    return "you didn't provide valid inputs"
 formated_f_name = f_name.title()
 formated_l_name = l_name.title()
 return f"hi! {formated_f_name} {formated_l_name}"
print(format_name(input("first name: "), input("last name: ")))

# returning function
def add(a, b):
    # returning sum of a and b
    return a + b

def is_true(a):
    # returning boolean of a
    return bool(a)
# calling function
res = add(2, 3)
print(res)
res = is_true(2<5)
print(res) 

# returning multiple values
def fun():
    name = "Alice"
    age = 30
    return name, age

name, age = fun()
print(name)  
print(age)   # Output: 30

# returning multiple values in a list
def fun_multiply(a, b):
    return [a * b, (a + b)*(a * b) ]
res = fun_multiply(2, 3)
print(res)  # Output: [6, 30]

# returning multiple values in a dictionary
def fun_1():
    def fun_2():
        def fun_3():
            return "hello"
        return fun_3()
    return fun_2()
res = fun_1()
print(res)  # Output: hello











# new_name = format_name("agrim", "jain")
# print(new_name)
# def function_1(text):
#  return text + text
# def function_2(text):
#  return text.title()
# output = function_2(function_1("agrim"))
# print(output)
