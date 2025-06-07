## treasure island ##
print("welcome to treasure island")
print("you're mission is to find the treasure . ")

choice1 = input("You\'re at a cross road . where do you want to go ? type 'left' or 'right' .")
if choice1 == "right":
    print(" you fell in a hole . game over")
else:
    choice2 = input('you are standing a corridoor . you see one "red door" and other is "blue door"? choose wisely ')
    if choice2 == "red":
        print("you won")
    else:
        print("you fell in a pool of crocs. you died")
