word_list = ["a", "abandon", "ability", "able", "abortion", "about", "above", "abroad", "absence", "absolute", "absolutely", "absorb", "abuse", "academic", "accept", "access", "accident", "accompany", "accomplish", "according", "account", "accurate", "accuse", "achieve", "achievement", "acid", "acknowledge", "acquire", "across", "act", "action", "active", "activist", "activity", "actor", "actress", "actual", "actually"]
import random
chosen_word = random.choice(word_list)
print(chosen_word)
placeholder = []
for letter in chosen_word:
    placeholder.append("_")
print(placeholder)
guess = input("guess a letter: ").lower()
print(guess)
for letter in chosen_word:
    if letter == guess:
        print("right")
    else:
        print("wrong")
