word_list = ["a", "abandon", "ability", "able", "abortion", "about", "above", "abroad", "absence", "absolute", "absolutely", "absorb", "abuse", "academic", "accept", "access", "accident", "accompany", "accomplish", "according", "account", "accurate", "accuse", "achieve", "achievement", "acid", "acknowledge", "acquire", "across", "act", "action", "active", "activist", "activity", "actor", "actress", "actual", "actually"]
import random
chosen_word = random.choice(word_list)
print(chosen_word)
placeholder = ''
for letter in chosen_word:
    placeholder += '_'
print(placeholder)
guess = input("guess a letter: ").lower()
print(guess)
for letter in chosen_word:
    if letter == guess:
        print("right")
    else:
        print("wrong")
def greet_with(name, location):
    print(f"hello {name}")
    print(f"what is like in {location}")
greet_with("agrim", "delhi")

def add(num1: int, num2: int) -> int:
    """Add two numbers"""
    num3 = num1 + num2

    return num3
# Driver code
num1, num2 = 5, 15
ans = add(num1, num2)
print(f"The addition of {num1} and {num2} results {ans}.")

# some more functions
def is_prime(n):
    if n in [2, 3]:
        return True
    if (n == 1) or (n % 2 == 0):
        return False
    r = 3
    while r * r <= n:
        if n % r == 0:
            return False
        r += 2
    return True
print(is_prime(78), is_prime(79))

