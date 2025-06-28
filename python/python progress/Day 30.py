# # file not found
# with open("Day 30.txt") as file:
#     file.read()

#key error
# dict = {"key": "value"}
# value = dict["non_existent_key"]

# #index error
# list = [1, 2, 3]
# value = list[5]

#type error
text = "Hello"
value = text + 5

try:
    file = open("Day 30.txt")
except FileNotFoundError:
    print("File not found. Please check the file path.")