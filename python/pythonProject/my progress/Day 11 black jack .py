''' doc string - triple quoted string
'''
def fun3(a,b):
    c = a / b
    return c
print(fun3(2,3))

def my_function():
    '''Demonstrates triple double quotes
    docstrings and does nothing really.'''
 
    return None

print("Using __doc__:")
print(my_function.__doc__)

print("Using help:")
help(my_function)

'''black jack game'''

import random
def deal_card():
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    card = random.choice(cards)
    return card
def calculate_score(cards):
    if sum(cards) == 21 and len(cards) == 2:
        return 0
    if 11 in cards and sum(cards) > 21:
        cards.remove(11)
        cards.append(1)
    return sum(cards)
def compare(user_score, computer_score):
    if user_score == computer_score:
        return "Draw"
    elif computer_score == 0:
        return "Lose, opponent has blackjack"
    elif user_score == 0:
        return "Win with a blackjack"
    elif user_score > 21:
        return "You went over, you lose"
    elif computer_score > 21:
        return "opponent went over, you win"
    elif user_score > computer_score:
        return "you win"
    else:
        return "you lose"






