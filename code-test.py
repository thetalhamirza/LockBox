import pwinput
user = input("Enter user: ")
password = pwinput.pwinput(mask='#')

print(user, password)