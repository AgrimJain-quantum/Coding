# todo
# to shoow the ascii art in the start of the game
# generate a random data for the game
# format the data into a prinatable format
# ask the user to guess which one has more followers
# check if the user is correct
## get follower count of the first and second data
## use if statement to compare the follower counts
# give feedback to the user
#  score keeping
# make the game repeatable
# making account at position b become the next account at position a 
import random
from art import logo, vs
from game_data import data
print(logo)
def format_data(account):
    account_name = account["name"]
    account_desc = account["description"]
    account_country = account["country"]
    return f"{account_name} , a {account_desc} , from {account_country}"

def check_answer(user_guess, a_followers , b_followers):
    if a_followers > b_followers:
        return user_guess == "a"
    else:
        return user_guess == "b"




account_a = random.choice(data)
account_b = random.choice(data)
if account_a == account_b:
    account_b = random.choice(data)



print(f"Compare A: {format_data(account_a)}.")
print(vs)
print(f"Against B: {format_data(account_b)}.")



guess = input("Who has more followers? Type 'A' or 'B': ").lower()




a_follower_count = account_a["follower_count"]
b_follower_count = account_b["follower_count"]

