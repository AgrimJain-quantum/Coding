with open(r"C:\Users\Agrim Jain\Desktop\Coding\python\pythonProject\my progress\my_file.txt", mode = "r") as file:    
    # # contents = file.read()
    # contents = file.write("This is a new line in the file.\n")
    # contents = file.write("This is another line in the file.\n")
    read_contents = file.read()
    print(read_contents)