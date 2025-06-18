# ''' doc string - triple quoted string
# '''
# def fun3(a,b):
#     c = a / b
#     return c
# print(fun3(2,3))

# def my_function():
#     '''Demonstrates triple double quotes
#     docstrings and does nothing really.'''
 
#     return None

# print("Using __doc__:")
# print(my_function.__doc__)

# print("Using help:")
# help(my_function)

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

def play_game():
    user_cards = []
    computer_cards = []
    for _ in range(2):
        user_cards.append(deal_card())
        computer_cards.append(deal_card())
        game_over = False
    while not game_over:
        user_score = calculate_score(user_cards)
        computer_score = calculate_score(computer_cards)
        print(f"your cards: {user_cards}, current_score: {user_score}")
        print(f"computer's first card: {computer_cards[0]}")
        if user_score == 0 or computer_score == 0 or user_score > 21:
            game_over = True
        else:
            should_continue = input("Type 'y' to get another card, type 'n' to pass: ")
            if should_continue == "y":
                user_cards.append(deal_card())
            else:
                game_over = True
    while computer_score != 0 and computer_score < 17:
        computer_cards.append(deal_card())
        computer_score = calculate_score(computer_cards)       
    print(f"   your final hand: {user_cards}, final score: {user_score}")
    print(f"   computer's final hand: {computer_cards}, final score: {computer_score}")
    print(compare(user_score, computer_score))
while input("Do you want to play a game of blackjack? Type 'y' or 'n': ") == "y":
    play_game()

# a = ['geeks' , 'for']
# a.append('geeks')
# a.append(['a' , 'coding ', 'platform'])
# print(a)

# b = ['agrim' , 'jain']
# a.extend(b)
# print(a)
# a.insert(20 , 'hello')
# print(a)

list  = [1, 2, 3, 4, 5, "agrim"]
# list.append(6)
# list.insert(0, 0)
# list.extend([7,8,9])
# list.remove(3)
# list.pop(-1)
# list.sort()
# list.reverse()
QWERTY = list.index("agrim")
print(QWERTY)

