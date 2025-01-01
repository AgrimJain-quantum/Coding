print("welcome to python pizza deliveries")
size = input("What size pizza do you want? S, M, or L ")
add_pepperoni = input("Do you want pepperoni? Y or N ")
extra_cheese = input("Do you want extra cheese? Y or N ")

# todo : work out how much they need to pay based on their size choice
# todo: work out how much to add to their bill based on their pepperoni choice
# todo: work out their final amount based on wherther thay want extra cheese or not

bill = 0
if size == "S":
    bill += 15
    if add_pepperoni == "Y":
        if size == "S":
            bill += 2
    else:
        bill +=3
    if extra_cheese == "Y":
        bill += 1
elif size == "M":
    bill += 20
elif size == "L":
    bill += 25
else:
    print("Invalid input .")
print(f"Your final bill is: ${bill}")



import random
random_heads_or_tails = random.randint(0,1)
if random_heads_or_tails == 1:
    print("Heads")
else:
    print("Tails")

people = ["Angela", "Ben", "Jenny", "Michael", "Chloe"]
#option 1
print(random.choice(people))
#option 2
rndom_index = random.randint(0,4)
print(people[rndom_index])
random.uniform(1,5)
print(random.uniform(1,5))  

student_scores = [78, 65, 89, 86, 55, 91, 64, 89]
max_score = 0
for score in student_scores:
    if score > max_score:
        max_score = score
print(max_score)

# fizz buzz game
for number in range(1, 101):
    if number % 3 == 0 and number % 5 == 0:
        print("FizzBuzz")
    elif number % 3 == 0:
        print("Fizz")
    elif number % 5 == 0:
        print("Buzz")
    else:
        print(number)
