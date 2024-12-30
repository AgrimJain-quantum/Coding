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