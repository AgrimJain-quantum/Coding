# number = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ]
# new_number = [n + 1 for n in number]
# name = "John"
# letter  = [letter  for letter in name]
# print(new_number)
# print(letter)
# range_list = [num * 2 for num in range (1, 11)]

# names = ["alex", "bob", "charlie", "dave"]
# short_names = [name for name in names if len(name)]
# print(range_list)
# print(short_names)

x = [y for y in range(1, 11)]
print(x)
w = [(x, y) for x in [1,2,3] for y in [3,1,4] if x != y]
print(w)
e = [(x, y) for x in [1,2,3] for y in [3,1,4] if x == y]
print(e)

