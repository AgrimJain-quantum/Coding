print("I am thinking of a word")
print("can you guess it?")
word = "python"
guesses = ""
turns = 10
while turns > 0:
    failed = 0
    for char in word:
        if char in guesses:
            print(char)
        else:
            print("_")
            failed += 1
    if failed == 0:
        print("you won")
        break
    guess = input("guess a character:")
    guesses += guess
    if guess not in word:
        turns -= 1
        print("wrong")
        print("you have", + turns, "more guesses")
        if turns == 0:
            print("you lose")
            print("the word was", word)
    
# print("hello" + input("what is your name?") + "!") 

# what = input("what is your name?")
# how = print("hello" + what + "!") 
# print(len(what)) # length of the name

# print(len(input("what is your name?"))) # length of the input statement
# lenght = len(input("what is your name?"))
# print(lenght) # length of the input statement

# print("hello"[4])
# print("hello"[0])
# print("hello"[1])
# print("hello"[2])
# print("hello"[3])
# print("hello"[4])
# print("hello"[-1])
# print("23456"[3])
# print(123_456_789) # this is a way to write a number with underscores
# print(123456789)
# print(123456789 + 123456789)
# print(3.14159)

# ## boolean data type
# print(True)
# print(False)
# print(3 > 5)
# print(3 < 5)
# print(3 == 5)
# print(3 >= 5)
# print(3 <= 5)
# print(123+456 == 123-456)
print(len("hello"))
