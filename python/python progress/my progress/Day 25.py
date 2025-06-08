# # with open (r"C:\Users\Agrim Jain\Desktop\Coding\python\python progress\my progress\weather_data.csv", "r") as file:
# #     data = file.readlines()
# #     print(data)

# import csv
# with open(r"C:\Users\Agrim Jain\Desktop\Coding\python\python progress\my progress\weather_data.csv", "r") as file:
#     data = csv.reader(file)
#     temperature = []
#     for row in data:
#         if row[1] != "temp":
#             temperature.append(int(row[1]))
#     print(temperature)

import pandas as pd
data = pd.read_csv(r"C:\Users\Agrim Jain\Desktop\Coding\python\python progress\my progress\weather_data.csv")
print(data)

