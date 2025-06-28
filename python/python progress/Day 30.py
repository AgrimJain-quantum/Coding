# # # file not found
# # with open("Day 30.txt") as file:
# #     file.read()

# #key error
# # dict = {"key": "value"}
# # value = dict["non_existent_key"]

# # #index error
# # list = [1, 2, 3]
# # value = list[5]

# #type error
# # text = "Hello"
# # value = text + 5

# try:
#     file = open("Day 30.txt")
# except :
#     file = open("Day 30.txt", "w")
#     file.write("This is a new file created because the original file was not found.")

#Exception Handling

# try:
#     file = open("a_file.txt")
#     a_dictionary = {"key": "value"}
#     print(a_dictionary["key"])
# except FileNotFoundError:
#     file = open("a_file.txt", "w")
#     file.write("Something")
# except KeyError as error_message:
#     print(f"The key {error_message} does not exist.")
# else:
#     content = file.read()
#     print(content)
# finally:
#     raise TypeError("This is an error message.")

#     file.close()
#     print("File was closed.")
# raise KeyError("This is an error message.")

height = float(input("Height: "))
weight = float(input("Weight: "))
if height > 3:
    raise ValueError("Height cannot be greater than 3 meters.")



bmi = weight / (height ** 2)
print(f"Your BMI is {bmi}")
