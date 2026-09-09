# # number = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ]
# # new_number = [n + 1 for n in number]
# # name = "John"
# # letter  = [letter  for letter in name]
# # print(new_number)
# # print(letter)
# # range_list = [num * 2 for num in range (1, 11)]

# # names = ["alex", "bob", "charlie", "dave"]
# # short_names = [name for name in names if len(name)]
# # print(range_list)
# # print(short_names)

# x = [y for y in range(1, 11)]
# print(x)
# w = [(x, y) for x in [1,2,3] for y in [3,1,4] if x != y]
# print(w)
# e = [(x, y) for x in [1,2,3] for y in [3,1,4] if x == y]
# print(e)

# import random
# names = ["alex", "bob", "charlie", "dave"]
# student_scores = {
#     "alex": 85,
#     "bob": 92,
#     "charlie": 78,
#     "dave": 88
# }
# scores = {student:random.randint(1,100) for student in names}
# student = {student:score for (student, score) in student_scores.items() if score >= 60}
# print(scores)
# print(student)


student_dict = {
    "student":["angela" , "james", "lily"],
    "score":[56, 76, 98]
}
# for (key, value) in student_dict.items():
    
#     print(key)
import pandas as pd
student_data_frame = pd.DataFrame(student_dict) 
print(student_data_frame)

for (index, row) in student_data_frame.iterrows():
    # print(index)
    # print(row)
    # print(row.student)
    print(row.score)
    