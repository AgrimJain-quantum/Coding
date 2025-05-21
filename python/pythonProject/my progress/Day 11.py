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












# new_name = format_name("agrim", "jain")
# print(new_name)
# def function_1(text):
#  return text + text
# def function_2(text):
#  return text.title()
# output = function_2(function_1("agrim"))
# print(output)
