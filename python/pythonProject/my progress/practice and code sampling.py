print(type("Hello"))
print(type(1))
print(type(1.0))
print(type(True))
print(type([1, 2, 3]))
print(type((1, 2, 3)))
print(type({"name": "John", "age": 23}))
print(type({1, 2, 3}))
print(type(None))
print(type(type))
print(type(print))
print(type(len))
print(type(type(1)))
int("123")
print(int("123"))   
print(int(123.45))

print("Number of letters in your name: " + str(len(input("What is your name? "))))

x = 5    # int
y = 2.0  # float
z = x + y  # Python implicitly converts x to float
print(z, type(z))  # Output: 7.0 <class 'float'>
print("x+y = " + str(z))
# Float to integer
x = 5.0    # float
y = 2.0    # float
z = x + y  # Python implicitly converts x and y to float
print(z, type(z))  # Output: 7.0 <class 'float'>
print("x+y = " + str(z))

num_str = "42"
num_int = int(num_str)
print(num_int, type(num_int))  # Output: 42 <class 'int'>

num = 5
num_float = float(num)
print(num_float, type(num_float))  # Output: 5.0 <class 'float'>

num = 10
num_str = str(num)
print(num_str, type(num_str))  # Output: "10" <class 'str'>

my_list = [1, 2, 3]
my_tuple = tuple(my_list)
print(my_tuple, type(my_tuple))  # Output: (1, 2, 3) <class 'tuple'>

my_tuple = (4, 5, 6)
my_list = list(my_tuple)
print(my_list, type(my_list))  # Output: [4, 5, 6] <class 'list'>

pairs = [("a", 1), ("b", 2)]
my_dict = dict(pairs)
print(my_dict, type(my_dict))  # Output: {'a': 1, 'b': 2} <class 'dict'>

text = "hello"
char_list = list(text)
print(char_list)  # Output: ['h', 'e', 'l', 'l', 'o']

print(6/2)
print(6//2)
print(6%2)
print(2*3)

text = "hello"
char_list = list(text)
print(char_list)  # Output: ['h', 'e', 'l', 'l', 'o']

print(6 // 2)
print(6 ** 2)
w = 3.14
q = int(w)
print(q)

print(3 * 3 + 3 / 3 - 3)
print(3 * (3 + 3) / 3 - 3)

print(3 * (3 + 3 / 3) - 3)
bmi = 84 / (1.8 ** 2)
print(bmi)
print(int(bmi))
print(round(bmi, 2))
water_level = int(input("Enter the water level: "))
if water_level > 80:
    print("Drain water")
else:
    print("Continue")
height = int(input("Enter your height in cm: "))
if height >= 120:
    print("You can ride the rollercoaster!")
else:  # Optional
    print("Sorry, you have to grow taller before you can ride.")
age = int(input("What is your age? "))
if age >= 18:
    print("You can drive at age 18.")
else:
    print("You cannot drive at age 18.")


num = int(input("Enter a number: "))
if num > 0:
    print("Positive number")
elif num == 0:  
    print("Zero")
else:
    print("Negative number")

count = 0
while count < 5:
    print(count)
    count += 1  
print("End of loop")

for i in range(5):
    print(i)
print("End of loop")
for i in range(10):
    if i == 5:
        break
    print(i)
# Output: 0 1 2 3 4

for i in range(10):
    if i == 5:
        continue
    print(i)

num = 10
if num > 0 and num % 2 == 0:
    print("Positive and even")
elif num > 0 and num % 2 != 0:
    print("Positive and odd")
else:
    print("Negative or zero")





print("Welcome to the rollercoaster!")
height  = int(input("What is your height in cm? "))
if height >= 120:
    print("you can ride the rollercoaster!")
    age = int(input("What is your age? "))
    if age < 12:
        bill = 5
        print("Please pay $5.")
    elif age <= 18:
        bill = 7
        print("Please pay $7.")
    elif age >= 45 and age <= 55:
        bill = 0
        print("Everything is going to be ok. Have a free ride on us!")
    else:
        bill = 12
        print("Please pay $12.")
    wants_input = input("Do you want a photo taken? type y for yes and n for no :")
    if wants_input == "y":
        bill += 3
    print(f"Your final bill is ${bill}")
else:
    print("Sorry, you have to grow taller before you can ride.")








    # Input for age and voter ID status
    age = int(input("Enter your age: "))
    has_voter_id = input("Do you have a voter ID? (yes/no): ").strip().lower()

    # Conditional checks
    if age >= 18:
        if has_voter_id == "yes":
            print("You can vote")
        else:
            print("You cannot vote because you do not have a voter ID")
    else:
        print("You cannot vote because you are underage")

    #input for weight and height
    weight = int(input("Enter your weight in kg: "))
    height = float(input("Enter your height in m: "))

    bmi = weight / (height ** 2)

    # 🚨 Do not modify the values above
    # Write your code below 👇
    if bmi < 18:
        print("underweight")
    elif bmi >= 18 and bmi < 25:
        print("normal weight")
    else:
        print("overweight")


class LinearCongruentialGenerator:
    def __init__(self, seed, a=1664525, c=1013904223, m=2**32):
        self.state = seed
        self.a = a
        self.c = c
        self.m = m
    
    def next(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state

# Initialize PRNG with a seed
seed = 42
lcg = LinearCongruentialGenerator(seed)

# Generate 10 pseudorandom numbers
for _ in range(10):
    print(lcg.next())




import sample_programs
print(sample_programs.bill)
print(sample_programs.size)
print(sample_programs.add_pepperoni)
print(sample_programs.extra_cheese)

random_number_0_to_1 = random.random() * 10
print(random_number_0_to_1)

random_float = random.uniform(1,10)
print(random_float)
 
import numpy as np
print(np.array([1, 2, 3]))
import random
fruits = ["Apple", "Banana", "Cherry"]
states_of_India = ["Karnataka", "Maharashtra", "Kerala", "Tamil Nadu", "Gujarat", "Rajasthan", "Uttar Pradesh", "Madhya Pradesh", "Bihar", "West Bengal", "Andhra Pradesh", "Telangna", "Odisha", "Assam", "Jharkhand", "Chhattisgarh", "Uttarakhand", "Himachal Pradesh", "Tripura", "Meghalaya", "Manipur", "Nagaland", "Goa", "Arunachal Pradesh", "Mizoram", "Sikkim", "Delhi", "Punjab", "Haryana", "Jammu and Kashmir", "Chandigarh", "Dadra and Nagar Haveli", "Daman and Diu", "Lakshadweep", "Puducherry", "Andaman and Nicobar Islands"]
print(random.choice(fruits))
print(random.choice(states_of_India))
print(states_of_India[2])
print(states_of_India[-1])
print(states_of_India[0:5])
print(states_of_India[:5])
print(states_of_India[5:])

mixed_list = [1, "Apple", 3.14, True]
print(mixed_list[1])
another_list = list([1.0,1.2,1.4,1.6,1.8,2.0])
print(another_list[0])
mixed_list.append("agrim")
print(mixed_list)
mixed_list.extend(another_list)
print(mixed_list)
mixed_list.insert(2, "Banana")
print(mixed_list)
my_list = [10, 20, 30]
for item in my_list:
    print(item)
# Output: 10, 20, 30
states_of_India.extend(mixed_list)
print(states_of_India)
states_of_India.remove("Apple")
print(states_of_India)


my_list = [10,20,30,40,50]
print(my_list[0])
print(my_list[-1])
my_list[1] = 25
print(my_list)

my_list.append(60)
print(my_list)
my_list.insert(2,15)
print(my_list)
my_list.extend([70,80,90])
print(my_list)
my_list.remove(40)
print(my_list)
my_list.pop(0)
print(my_list)
my_list.sort()
print(my_list)
my_list.reverse()
print(my_list)
my_list.clear()
print(my_list)
my_list.count(20)
print(my_list)
my_list.copy()
print(my_list)

my_list = [10, 20, 30]
for item in my_list:
    item += 1
    print(item)
# Output: 10, 20, 30


import random 
dirty_dozen = ["strawberries", "spinach" , "kale" , "nectarines" , "apples"]
friuts = ["apples", "oranges", "bananas", "grapes", "mangoes"]
vegetables = ["spinach", "kale", "carrots", "tomatoes", "potatoes"]
dirty_dozen.extend(friuts)
print(dirty_dozen)
print(random.randint(1, 6))
# Output: Random number between 1 and 6

import string
characters = string.ascii_letters + string.digits + string.punctuation
password = ''.join(random.choices(characters, k=12))
print(password)  # Example: 'aZ3!bX9@Lm2#'

fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)
    print(fruit + " pie")
    print(fruit + " juice")
    print(fruits)


print(range(1, 100))
no_of_students = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
for student in no_of_students:
    print(student)

# total = 0
# for no in range(0, 11 ,2):
#     total += no
# print(total)

total = 0
for number in range(1, 101):
    total += number
print(total)


while True:
    response = input("Type 'exit' to stop: ")
    if response == "exit":
        break

for i in range(5):
    if i == 3:
        continue
    print(i)

total = sum(range(1, 6))
print(total)
# Output: 15 (1 + 2 + 3 + 4 + 5)

fruits = ["apple", "banana", "cherry"]
for i in range(len(fruits)):
    print(f"Index {i}: {fruits[i]}")


len("hello")
n = 5
factorial = 1
for i in range(1, n + 1):
    factorial *= i
print("Factorial:", factorial)  # Output: 120

numbers = [1, 2, 3, 4, 5]
search = 3
for num in numbers:
    if num == search:
        print("Found:", num)
        break

def greet():
    print("Hello")
    print("Good Morning")
greet()

def greet(name):
    print(f"Hello, {name}!")

greet("Agrim")
# Output: Hello, Agrim!
