## tip calculator ## 
print("welcome to tip calculator")
bill = float(input("what is the total bill? "))
tip = int(input("what is the percentage of tip would you like to give? 10, 12 or 15 "))
people = int(input("How many people you want to split the bill ?"))
total_bill_with_tip = bill + tip/100 * bill
bill_split = total_bill_with_tip/people
print(f"the total bill is: {total_bill_with_tip} ")
print(f"the splitted bill is : {bill_split} ")