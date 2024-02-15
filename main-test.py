from cryptography.fernet import Fernet
import sys


global auth
pfile = "passwords.txt"
keydata = "keydata.txt"
auth = False

###

def main():
    global auth
    if not auth:
        initialize_user()
        auth = True
    
    print_menu()
    choice = get_user_choice()
    execute_choice(choice)

def initialize_user():
    initMasterKey()
    user_type = authorize()
    initializeKeys(user_type)

def print_menu():
    print()
    print("Menu:\n")
    print("1: Add a new password")
    print("2: Retrieve a password")
    print("3: Delete an existing password (Code in progress)")
    print("4: Generate a new password (Code in progress)")
    print("0: Exit")
    print()

def get_user_choice():
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if choice not in [0, 1, 2, 3, 4]:
                raise ValueError("Invalid choice. Please enter a number from the menu.")
            return choice
        except ValueError as e:
            pass
        except KeyboardInterrupt:
            sys.exit("\nExiting...")

def execute_choice(choice):
    match choice:
        case 1: 
            addPassword()
        case 2: 
            retrievePassword()
        case 3:
            print("Deleting password... (Code in progress)")
        case 4:    
            print("Generating new password... (Code in progress)")
        case 0:
            sys.exit('Exiting...')

###

def addPassword():
    user = input("Enter a username/email/website: ")
    while True:    
        try:
            pwd = input("Enter a password to add: ")
            if pwd != '':
                break
            else:
                print("Password cannot be blank. Press Ctrl-c to go to main menu")
        except KeyboardInterrupt:
            main()    
    if validation(pwd):
        encrypted_user = encrypt(user).decode('utf8')
        encrypted_pwd = encrypt(pwd).decode('utf8')
        with open(pfile, 'a') as f:
            f.write(f"{encrypted_user}|,|{encrypted_pwd}\n")
        print("\nAdded!\n")
    main()


def retrievePassword():
    global masterPass
    lines = []
    with open(pfile, 'r') as f:
        for line in f:
            lines.append(line)
    if len(lines) > 0:
        userchoice = input("Enter the username/email/website you need the password for: ")
        found = False
        try:
            for current in lines:
                user, pwd = current.replace('\n','').split('|,|')
                decUser= fernet.decrypt(user).decode('utf8')
                if decUser == userchoice:
                    decPwd= fernet.decrypt(pwd).decode('utf8')
                    if input("Enter the master password: ") == masterPass:
                        print()
                        print(f"User: {decUser}")
                        print(f"Password: {decPwd}")
                        print()
                        found = True
                        break
        except fernet.InvalidToken:
            print("Fernet Token Error. Code needs debugging")


        if not found: print("\nUsername not found\n")
    else:
        print("\nNo credentials currently stored.\n")
    main()



def encrypt(password):
    cipher = fernet.encrypt(password.encode())
    return cipher


def decrypt(cipher):
    global fernet
    decipher = fernet.decrypt(cipher).decode()
    return decipher
    

def authorize():            
    global masterFernet
    global masterPass
    lines = []
    with open(keydata, 'r') as f:
        for line in f:
            lines.append(line)
    if len(lines) == 1:
        print("Let's create your account")
        newUser = input("Enter a new username: ")
        newPass = input("Enter a new password: ")
        masterPass = newPass
        encUser = masterFernet.encrypt(newUser.encode())
        encPass = masterFernet.encrypt(newPass.encode())
        with open(keydata, 'a') as f:
            f.write(f'user: {encUser}|,|pass: {encPass}\n')       
            return 'newUser'
    else:
        try:
            checkuser, checkpwd = lines[1].replace('\n','').split('|,|')
            checkuser = checkuser.replace('user: ','')
            checkpwd = checkpwd.replace('pass: ','')
            decUser = masterFernet.decrypt(bytes(checkuser[2:-1], encoding='utf8').decode()).decode()
            decPwd = masterFernet.decrypt(bytes(checkpwd[2:-1], encoding='utf8').decode()).decode()
        except ValueError:
            sys.exit("error: check keydata file")
        user = input("Enter a username: ")
        masterPass = input("Enter a password: ")
        if user == decUser:
            if masterPass == decPwd:                  
                print("\nAuthorised\n")
                return 'existingUser'
            else:
                sys.exit("\nWrong credentials, please try again\n")           #maybe give them another chance?
        else:
            sys.exit("\nWrong credentials, please try again\n")           #maybe give them another chance?
            

def initializeKeys(choice):
    global fernet
    if choice == 'newUser':
        key = Fernet.generate_key()
        with open(keydata, 'a') as f:
            f.write(f'key: {key}\n')
        fernet = Fernet(bytes(key))
    elif choice == 'existingUser':
        with open(keydata, 'r') as f:
            for line in f:
                if 'key' in line:
                    key = line[5:]
                    fernet = Fernet(bytes(key[2:-1], encoding='utf8'))
                    break

def initMasterKey():
    global masterFernet
    with open(keydata, 'r') as f:
        lines = []
        for line in f:
            lines.append(line)
    if len(lines) >= 1 and lines[0][:10] == 'masterKey:':
        masterKey = bytes(lines[0][11:], encoding='utf8').decode()
        masterFernet = Fernet(bytes(masterKey[2:-1], encoding='utf8'))
    else:
        masterKey = Fernet.generate_key()
        masterFernet = Fernet(masterKey)
        with open(keydata, 'a') as f:
            f.write(f"masterKey: {masterKey}\n")

def validation(password):
    if len(password) < 8:
        print("\nWarning: Password must be of at least 8 characters\n")
        return False

    lowercount = sum(1 for char in password if char.islower())
    uppercount = sum(1 for char in password if char.isupper())
    numcount = sum(1 for char in password if char.isdigit())
    if lowercount >= 1 and uppercount >= 1 and numcount >= 1:
        print("\nSuccess: Password passes the security check\n")
        return True
    else:
        while True:
            inChoice = input("Warning: Password is not secure. Continue? (Y/N): ")
            if inChoice == "Y":
                return True
            elif inChoice == "N":
                break
    # return True

if __name__ == "__main__":
    main()