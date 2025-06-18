# # # # # # # # with open (r"C:\Users\Agrim Jain\Desktop\Coding\python\python progress\my progress\weather_data.csv", "r") as file:
# # # # # # # #     data = file.readlines()
# # # # # # # #     print(data)

# # # # # # # import csv
# # # # # # # with open(r"C:\Users\Agrim Jain\Desktop\Coding\python\python progress\my progress\weather_data.csv", "r") as file:
# # # # # # #     data = csv.reader(file)
# # # # # # #     temperature = []
# # # # # # #     for row in data:
# # # # # # #         if row[1] != "temp":
# # # # # # #             temperature.append(int(row[1]))
# # # # # # #     print(temperature)

# # # # # # # import pandas as pd
# # # # # # # data = pd.read_csv(r"C:\Users\Agrim Jain\Desktop\Coding\python\python progress\my progress\weather_data.csv")
# # # # # # # print(type(data["temp"]))
# # # # # # # print(data["temp"].mean())

# # # # # # import pandas as pd
# # # # # # a = [1, 7, 2]
# # # # # # myvar = pd.Series(a)
# # # # # # print(myvar)
# # # # # # print(myvar[0])
# # # # # # print(myvar[1])
# # # # # # print(myvar[2])
# # # # # # print(myvar[1:3])
# # # # # # # print(myvar[1:])  # Slicing from index 1 to the end

# # # # # import pandas as pd
# # # # # a = [1, 7, 2]
# # # # # myvar = pd.Series(a, index = ["x", "y", "z"])
# # # # # # print(myvar)

# # # # import pandas as pd
# # # # data = pd.read_csv(r"C:\Users\Agrim Jain\Desktop\Coding\python\python progress\my progress\weather_data.csv")
# # # # print(type(data["temp"]))
# # # # print(data["temp"].mean())
# # # # print(data["temp"].max())
# # # # x = data["day"]
# # # # print(x)


# # import pandas as pd
# # months_days = {    "January": 31,
# #     "February": 28,
# #     "March": 31,
# #     "April": 30,
# #     "May": 31,
# #     "June": 30,
# #     "July": 31,
# #     "August": 31,
# #     "September": 30,
# #     "October": 31,
# #     "November": 30,
# #     "December": 31
#     }

# # # var = pd.Series(months_days)
# # # print(var)
# # # var_1 = pd.Series(months_days, index=["January", "March", "May", "July", "August", "October"])
# # # print(var_1)  

# # import pandas as pd
# # data = pd.read_csv(r"C:\Users\Agrim Jain\Desktop\Coding\python\python progress\my progress\weather_data.csv")
# # data_dict = data.to_dict()
# # print(data_dict)
# # x = data["temp"].to_list()
# # print(x)
# import pandas as pd
# data = pd.read_csv(r"C:\Users\Agrim Jain\Desktop\Coding\python\python progress\my progress\weather_data.csv")
# # data_dict = data.to_dict()
# # temp_list = data["temp"].to_list()
# # length = len(temp_list)
# # mean = data["temp"].mean()
# # max = data["temp"].max()
# # print(f"all the detailes of the given data is:  {data_dict}")
# # print(f"the list of all the temperature is: {temp_list}")
# # print(f"the length of the temperature list is: {length}")
# # print(f"the mean of the temperature is: {mean}")
# # print(f"the maximum temperature is: {max}")
# # print(data["condition"])
# # print(data.condition)
# # print(data[data.day == "Monday"])

# # print(data[data.temp == data.temp.max()])
# # print(data[data.temp == data.temp.min()])
# # print(data[data.day == "Monday"])
# monday = data[data.day == "Monday"]
# monday_temp = monday.temp[0]
# monday_temp_f = monday_temp * 9/5 + 32
# print(f"Monday's temperature in Fahrenheit is: {monday_temp_f}")

# data_dict_2 = {
#     "names": ["Agrim", "Aarav", "Aarvi"],
#     "scores": [100, 90, 80],
#     "grades": ["A+", "A", "B+"]
# }
# details = pd.DataFrame(data_dict_2) 
# details.to_csv("details.csv")

import pandas as pd
data  = pd.read_csv(r"C:\Users\Agrim Jain\Desktop\Coding\python\2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv") 
grey_squirrels_count = len(data[data["Primary Fur Color"] == "Gray"])
red_squirrels_count = len(data[data["Primary Fur Color"] == "Cinnamon"])
black_squirrels_count = len(data[data["Primary Fur Color"] == "Black"])

print(f"Number of gray squirrels: {grey_squirrels_count}")
print(f"Number of red squirrels: {red_squirrels_count}")    
print(f"Number of black squirrels: {black_squirrels_count}")

data_dict = {
    "Fur Color": ["Gray", "Red", "Black"],
    "Count": [grey_squirrels_count, red_squirrels_count, black_squirrels_count],
}
re = data.corr()
print(re)
print(data_dict)


