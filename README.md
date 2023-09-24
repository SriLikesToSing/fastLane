# fastLane 

<img src="https://github.com/SriLikesToSing/fastLane/blob/main/src/fastLane.png" width="300" height="300">

FastLane is a stateless and serverless password manager. Use only one password to get access to all of your passwords without storing all of them using a database. Uses a sha512 hashing algorithm to create a new password using your master password. This makes using a database to store your other passwords uncessesary and increases ease of use and security. 

Features:

  - Generate master password using random.com which then goes through a sha512 hashing algorithm to create the most secure master password. 
  
 - Generate special passwords for certain websites using the master password and eliminate the need to store them because they are all generated using the masterpassword
   
- Never memorize multiple passwords or fear someone hacking into servers and gaining access to all your password stores. Your passwords for your websites are mathematically connected to your master password enstead of your passwords being accessed through a database which is extremely more unsafe. 

## How it Works

The password generator uses the following components:

1. **Character Subsets:** The script defines several character subsets, including lowercase letters, uppercase letters, digits, and symbols. These subsets are used to build the characters for the generated password.

2. **Entropy Calculation:** The script calculates entropy by hashing the master password along with site-specific and login-specific information using the PBKDF2-HMAC-SHA512 algorithm. This step helps in generating a unique password for each combination of site and login.

3. **Password Generation:** The script generates a password based on the calculated entropy. It follows these steps:
   - It determines the character set based on the selected rules (e.g., lowercase, uppercase, digits, symbols) and excludes any characters specified to be excluded.
   - It generates a password by repeatedly consuming entropy to select characters from the character set until it reaches the desired password length.
   - It ensures that at least one character from each selected rule is included in the password.

4. **User Interface:** The script provides a simple command-line interface for generating passwords, logging in, and quitting.


## Usage

# Windows

```bash
  download and click on main.exe 
```

# Linux

```bash
  sudo apt-get install wine
  wine dir_to_program/main.exe
```
- Select 1 if you want to generate a master password
  
1. Select option 2 to log in.

2. Provide the following details:
    - Site: example.com
    - Login: user@example.com
    - Rules: lowercase, uppercase, digits, symbols (include whatever you want, and leave blank if you want all rules) 
    - Exclusion: (exclude from any of the above)
    - Length: (your preferred length)
  
3. Enter your master password when prompted.

4. The script will generate and display a strong and secure password for the specified site and login.

# Important Security Note
The generated passwords are as secure as your master password location. Ensure that your master password is kept confidential. Never share your master password or store it in an insecure location.


[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)

