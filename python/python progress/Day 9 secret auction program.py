""" secret auction program """

name = input("what is your name ?")
price = int(input("place your bid : "))
bids = {}
bids[name] = price
should_continue = input("do you want to continue ? yes or no \n")
continue_bidding = True

while should_continue == "yes":
    name = input("what is your name ?")
    price = int(input("place your bid : "))
    bids[name] = price
    should_continue = input("do you want to continue ? yes or no \n")
    if should_continue == "no":
        continue_bidding = False
    elif should_continue == "yes":
        continue_bidding = True
    else:
        print("please enter yes or no")
        continue_bidding = True
def find_highest_bidder(bidding_record):
    highest_bid = 0
    winner = ""
    for bidder in bidding_record:
        bid_amount = bidding_record[bidder]
        if bid_amount > highest_bid:
            highest_bid = bid_amount
            winner = bidder
    print(f"The winner is {winner} with a bid of {highest_bid}")
find_highest_bidder(bids)