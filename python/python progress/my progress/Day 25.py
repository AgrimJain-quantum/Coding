# with open (r"C:\Users\Agrim Jain\Desktop\Coding\python\python progress\my progress\weather_data.csv", "r") as file:
#     data = file.readlines()
#     print(data)

import csv
with open(r"C:\Users\Agrim Jain\Desktop\Coding\python\python progress\my progress\weather_data.csv", "r") as file:
    data = csv.reader(file)
    print(data)