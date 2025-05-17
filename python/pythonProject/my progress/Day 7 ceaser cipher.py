alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")
text = input("Type your message:\n").lower()
shift = int(input("Type the shift number:\n"))

def caesar(original_text, shift_amount ):
    cipher_text = ""
    for letter in original_text:
        shifted_position = alphabet.index(letter) + shift_amount
        if shifted_position > len(alphabet) - 1:
            shifted_position = shifted_position - len(alphabet)
        cipher_text += alphabet[shifted_position]
    print(f"Here is the encoded result: {cipher_text}")

def caesar_decode(original_text, shift_amount):

def caesar_cipher(text, shift, direction):
    result = ""
    for char in text:
        if char.isalpha():
            # Keep the case (upper/lower)
            offset = 65 if char.isupper() else 97
            shifted = ((ord(char) - offset + shift * (1 if direction == "encode" else -1)) % 26) + offset
            result += chr(shifted)
        else:
            result += char  # Keep spaces, punctuation, etc. unchanged
    print(result)
