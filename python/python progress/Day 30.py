
try:
    file = open("a_day30.txt")
except:
    file = open("a_day30.txt", "w")
    file.write("This is a new file created by the code.")
    file.close()
    file = open("a_day30.txt") 