import random

rock = '''
██████████████████████████
█▄─▄▄▀█─▄▄─█─▄▄▄─█▄─█─▄███
██─▄─▄█─██─█─███▀██─▄▀████
▀▄▄▀▄▄▀▄▄▄▄▀▄▄▄▄▄▀▄▄▀▄▄▀▀▀
'''
paper = '''
█████████████████████████████████
█▄─▄▄─██▀▄─██▄─▄▄─█▄─▄▄─█▄─▄▄▀███
██─▄▄▄██─▀─███─▄▄▄██─▄█▀██─▄─▄███
▀▄▄▄▀▀▀▄▄▀▄▄▀▄▄▄▀▀▀▄▄▄▄▄▀▄▄▀▄▄▀▀▀
'''
scissors = '''
██████████████████████████████████████████████
█─▄▄▄▄█─▄▄▄─█▄─▄█─▄▄▄▄█─▄▄▄▄█─▄▄─█▄─▄▄▀█─▄▄▄▄█
█▄▄▄▄─█─███▀██─██▄▄▄▄─█▄▄▄▄─█─██─██─▄─▄█▄▄▄▄─█
▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▄▀▄▄▀▄▄▀▄▄▄▄▄▀
'''

gameimages = [rock, paper, scissors]

player_choice = int(input("What do you choose? Type 0 for Rock, 1 for Paper, and 2 for Scissors: "))

# Validate player choice
if player_choice < 0 or player_choice >= 3:
    print("You typed an invalid number. You lose!")
else:
    print(gameimages[player_choice])

    # Generate and display bot's choice
    bot_choice = random.randint(0, 2)
    print("Computer chose:")
    print(gameimages[bot_choice])

    # Determine the result
    if player_choice == bot_choice:
        print("It's a draw!")
    elif (player_choice == 0 and bot_choice == 2) or \
         (player_choice == 1 and bot_choice == 0) or \
         (player_choice == 2 and bot_choice == 1):
        print("You win!")
    else:
        print("You lose!")
