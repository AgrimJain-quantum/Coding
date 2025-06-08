# # # # with open (r"C:\Users\Agrim Jain\Desktop\Coding\python\python progress\my progress\weather_data.csv", "r") as file:
# # # #     data = file.readlines()
# # # #     print(data)

# # # import csv
# # # with open(r"C:\Users\Agrim Jain\Desktop\Coding\python\python progress\my progress\weather_data.csv", "r") as file:
# # #     data = csv.reader(file)
# # #     temperature = []
# # #     for row in data:
# # #         if row[1] != "temp":
# # #             temperature.append(int(row[1]))
# # #     print(temperature)

# # # import pandas as pd
# # # data = pd.read_csv(r"C:\Users\Agrim Jain\Desktop\Coding\python\python progress\my progress\weather_data.csv")
# # # print(type(data["temp"]))
# # # print(data["temp"].mean())

# # import pandas as pd
# # a = [1, 7, 2]
# # myvar = pd.Series(a)
# # print(myvar)
# # print(myvar[0])
# # print(myvar[1])
# # print(myvar[2])
# # print(myvar[1:3])
# # # print(myvar[1:])  # Slicing from index 1 to the end

# import pandas as pd
# a = [1, 7, 2]
# myvar = pd.Series(a, index = ["x", "y", "z"])
# # print(myvar)

import pandas as pd
data = pd.read_csv(r"C:\Users\Agrim Jain\Desktop\Coding\python\python progress\my progress\weather_data.csv")
print(type(data["temp"]))
print(data["temp"].mean())
print(data["temp"].max())
x = data["day"]
print(x)