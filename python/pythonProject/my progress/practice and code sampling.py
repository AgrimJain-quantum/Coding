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
        print("Please pay $5.")
    elif age <= 18:
        print("Please pay $7.")
    else:
        print("Please pay $12.")
else:
    print("Sorry, you have to grow taller before you can ride.")

if age >= 18:
    if has_voter_id:
        print("You can vote")
    else:
        print("You cannot vote")
else:
    print("You cannot vote")