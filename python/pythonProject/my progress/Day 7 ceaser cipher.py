# alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
# direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")
# text = input("Type your message:\n").lower()
# shift = int(input("Type the shift number:\n"))
# def encrypt(original_text, shift_amount):
#     cipher_text = ""
#     for letter in original_text:
#         shifted_position = alphabet.index(letter) + shift_amount
#         cipher_text += alphabet[shifted_position]
#     print(f"The encoded text is {cipher_text}")
# encrypt(text, shift)

# def decrypt(original_text, shift_amount):
#     decipher_text = ""
#     for letter in original_text:
#         shifted_position = alphabet.index(letter) - shift_amount
#         decipher_text += alphabet[shifted_position]
#     print(f"The decoded text is {decipher_text}")
# decrypt(text, shift)


# def add(*args):
#     return sum(args)
# print(add(1,2,3,4,5))

# def full_name(first,last):
#     print(f"hi my first name is {first}")
#     print(f"my last name is {last}")
# full_name("john", "doe")
# full_name("jain" , "agrim")

# print("hello" [1])
# print("hello" [0])
# print("hello" [2])  
# print("hello" [3])

# interger = 123
# float = 1.23
# new_number = interger + float
# print(new_number)
# print(type(new_number))

# def f1():
#     a = 1
#     def f2():
#         print(a)
#     f2()
# f1()
# def my_function(*args):
#     for arg in args:
#         print(arg)
# my_function(1, 2, 3, 4, 5)
def my_function(arg1, *args):
    print("funtion :" , arg1)
    for arg in args:
        print("my_secondarg : ", arg)
my_function(1, 2, 3, 4, 5)


