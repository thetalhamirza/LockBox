# LockBox

LockBox is a command-line password manager built with Python. It allows you to securely store and manage your passwords. This is my final project for CS50p, and I hope you'll like it :)

## Features

- Add, retrieve, and delete passwords for different accounts.
- Generate strong passwords.
- View all stored usernames.
- Passwords are encrypted using the Fernet encryption scheme.

## Installation

1. Clone the repository:
```sh
   git clone https://github.com/thetalhamirza/LockBox.git
```
2. Install the required dependencies:
```sh
  pip install -r requirements.txt
```
3. Run the program
```sh
  python lockbox.py
```


## Usage
- To add a new password, choose option 1 from the menu and follow the prompts.
- To retrieve a password, choose option 2 and enter the username/email/website.
- To delete a password, choose option 3 and follow the prompts.
- To view all stored usernames, choose option 4
- To generate a random password, choose option 5

## Security
- Passwords are encrypted using the Fernet encryption scheme.
- Master passwords are securely stored.

## Contributing

Contributions are welcome! There is a lot of room for improvement in this code.
Fork the repository and submit a pull request to do your part.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements
- Thanks to the cryptography library for providing the encryption functionality.
- Thanks to the pwinput library for providing password input functionality.
