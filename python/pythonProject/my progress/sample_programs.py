# print("welcome to python pizza deliveries")
# size = input("What size pizza do you want? S, M, or L ")
# add_pepperoni = input("Do you want pepperoni? Y or N ")
# extra_cheese = input("Do you want extra cheese? Y or N ")

# # todo : work out how much they need to pay based on their size choice
# # todo: work out how much to add to their bill based on their pepperoni choice
# # todo: work out their final amount based on wherther thay want extra cheese or not

# bill = 0
# if size == "S":
#     bill += 15
#     if add_pepperoni == "Y":
#         if size == "S":
#             bill += 2
#     else:
#         bill +=3
#     if extra_cheese == "Y":
#         bill += 1
# elif size == "M":
#     bill += 20
# elif size == "L":
#     bill += 25
# else:
#     print("Invalid input .")
# print(f"Your final bill is: ${bill}")



# import random
# random_heads_or_tails = random.randint(0,1)
# if random_heads_or_tails == 1:
#     print("Heads")
# else:
#     print("Tails")

# people = ["Angela", "Ben", "Jenny", "Michael", "Chloe"]
# #option 1
# print(random.choice(people))
# #option 2
# rndom_index = random.randint(0,4)
# print(people[rndom_index])
# random.uniform(1,5)
# print(random.uniform(1,5))  

import random
items = ["apple", "banana", "cherry"]
print(random.choices(items, weights=[1, 2, 3], k=5))  # Example: ['cherry', 'banana', 'cherry', 'apple', 'cherry']

deck = [1, 2, 3, 4, 5]
random.shuffle(deck)
print(deck)  # Example: [3, 1, 5, 2, 4]


states_of_India = ["Karnataka", "Maharashtra", "Kerala", "Tamil Nadu", "Gujarat", "Rajasthan", "Uttar Pradesh", "Madhya Pradesh", "Bihar", "West Bengal", "Andhra Pradesh", "Telangna", "Odisha", "Assam", "Jharkhand", "Chhattisgarh", "Uttarakhand", "Himachal Pradesh", "Tripura", "Meghalaya", "Manipur", "Nagaland", "Goa", "Arunachal Pradesh", "Mizoram", "Sikkim", "Delhi", "Punjab", "Haryana", "Jammu and Kashmir", "Chandigarh", "Dadra and Nagar Haveli", "Daman and Diu", "Lakshadweep", "Puducherry", "Andaman and Nicobar Islands"]
random.shuffle(states_of_India)
print(states_of_India)
print(random.sample(states_of_India, k=5))  # Example: ['Karnataka', 'Maharashtra', 'Kerala', 'Tamil Nadu', 'Gujarat']