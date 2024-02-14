from cryptography.fernet import Fernet
import sys


global auth
pfile = "passwords.txt"
keydata = "keydata.txt"
auth = False

def main():
    global auth
    if not auth:
        initMasterKey()
        userType = authorize()
        
        initializeKeys(userType)
        auth = True
    print("1: Add a new password")
    print("2: Retrieve a password")
    print("3: Delete an existing password")
    print("4: Generate a new password")
    print("0: Exit")
    choice = int(input("Enter a choice: "))
    match choice:
        case 1: 
            addPassword(input("Enter a username/email/website: "), input("Enter a password to add: "))
        case 2: 
            retrievePassword()
        case 3:
            print('Code in progress')
            main()
        case 4:    
            print('Code in progress')
            main()
        case 0:
            sys.exit('Exiting...')


def addPassword(user, pwd):
    if validation(pwd):
        with open(pfile, 'a') as f:
            f.write(f"user={encrypt(user).decode('utf8')}|,|pass={encrypt(pwd).decode('utf8')}\n")
    main()

def retrievePassword():
    global masterPass
    lines = []
    with open(pfile, 'r') as f:
        for line in f:
            lines.append(line)
    if len(lines) > 0:
        userchoice = input("Enter the username/email/website you need the password for: ")
        for current in lines:
            user, pwd = current.replace('\n','').split('|,|')
            user = user.replace('user=','')
            pwd = pwd.replace('pass=','')
            decUser= fernet.decrypt(user).decode('utf8')
            if decUser == userchoice:
                decPwd= fernet.decrypt(pwd).decode('utf8')
                if input("Enter the master password: ") == masterPass:
                    print(decUser)
                    print(decPwd)
            else:
                print("Username not found")
    else:
        print("No credentials currently stored.")
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
                print("Authorised\n")
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
        




def validation(password):           ###
    # lowercount = 0
    # uppercount = 0
    # numcount = 0
    # for char in password:
    #     if char >= 'a' and char <= 'z':
    #         lowercount += 1
    #     elif char >= 'A' and char <= 'Z':
    #         uppercount += 1
    #     elif char >= '0' and char <= '9':
    #         numcount += 1
            
    # if len(password) < 8:
    #     return False
    # elif lowercount >= 1 and uppercount >= 1 and numcount >= 1:
    #     return True
    return True

if __name__ == "__main__":
    main()