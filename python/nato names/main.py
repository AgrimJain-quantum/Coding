# #TODO 1. Create a dictionary in this format:
# {"A": "Alfa", "B": "Bravo"}
# #TODO 2. Create a list of the phonetic code words from a word that the user inputs.

import pandas as pd
data = pd.read_csv(r"C:\Users\Agrim Jain\Desktop\Coding\python\nato names\nato_phonetic_alphabet.csv")
print(data.to_dict())
phonetic_dict = {row.letter: row.code for (index, row) in data.iterrows()}
print(phonetic_dict)

word = input("enter a word: ").upper()
output_list = [phonetic_dict[letter] for letter in word]
