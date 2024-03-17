# import secrets
# import string
# import random
import sys


# letters = string.ascii_letters

# digits = string.digits

# special_chars = string.punctuation

# selection_list = letters + digits + special_chars

# password_len = 10

# password = ''
# for i in range(password_len):
#     password += ''.join(secrets.choice(selection_list))

# print(password)


def executeChoice(choice):
    match choice:
        case 1: 
            # addPassword()
            print('a')
        case 2: 
            # retrievePassword()
            print('a')
        case 3:
            # deletePassword()
            print('a')
        case 4:    
            # generatePassword()
            print('a')
        case 0:
            print()
            sys.exit('Exiting...')
        case _:
            raise ValueError

executeChoice(66)