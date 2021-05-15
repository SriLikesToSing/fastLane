import hashlib
import click
import quantumrandom


#Programming a better password manager from scratch

#first time users can use an inbuilt password generator
#make command line and gui version
'''
use kivy for gui
    - https://kivy.org/#home
    - https://kivy.org/#gallery


'''

'''
fastLane: a open source self hosted offline password manager that requires no database

self hosted
maybe:
    configures the self hostedness automatically so that if you have this system installed on multiple systems

how do I add extra security:
    if more than three tries then send notif to phone
        if not then lock out the password manager

can you make the password management system better?
    - currently modifying and using algorithms based on lesspass (I will mostly change this)

shows all the usernames and logins that are currently in the system once your logged in (optional: on by default)

settings menu

two factor authentication?
    - phone notification

use an external drive process option to safely store the program to quickly use it on other devices

option to remember the password so you dont have to type it in every time (so you only need to type in the login, username, and any characters you want taken out)
    - can choose to forget it after some time period

Password generator functions
'''

CHARACTER_SUBSETS = {
    "lowercase":"abcdefghijklmnopqrstuvwxyz",
    "uppercase":"ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "digits":"0123456789",
    "symbols":"!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

}


def calcEntropy(passwordProfile, masterPassword):
    salt = (
        passwordProfile["site"]
        + passwordProfile["login"]
        )

    hexEntropy = hashlib.pbkdf2_hmac("sha512", masterPassword.encode("utf-8"), salt.encode("utf-8"), 100000, 32).hex()
    #return hexEntropy
    return int(hexEntropy, 16)

def removeExcludedChars(string, exclude):
    strList = list(string)
    excludedString = ""

    for char in string:
        if char in exclude:
            continue
        else:
            excludedString+=char
    return excludedString


def getCharacters(rules=None, exclude=""):
    #Get the character set to make the password
    if rules is None:
        return(CHARACTER_SUBSETS["lowercase"]+CHARACTER_SUBSETS["uppercase"]+CHARACTER_SUBSETS["digits"]+CHARACTER_SUBSETS["symbols"])
    charList = ""

    for rule in rules:
       charList+=CHARACTER_SUBSETS[rule]
    return removeExcludedChars(charList, exclude)

def consumeEntropy(generatedPassword, quotient, characterSet, maxLength):
    if len(generatedPassword) >= maxLength:
        return [generatedPassword, quotient]
    #div mod returns two integers quotient q and remainder
    #quotient is the large number
    quotient, remainder = divmod(quotient, len(characterSet))
    #print(remainder)
    #basically converts the numbers into the character set
    generatedPassword+= characterSet[remainder]
    return consumeEntropy(generatedPassword, quotient, characterSet, maxLength)

def insertStringPseudoRandomly(generatedPassword, entropy, string):
    #inserts string accordings to sha256 psuedorandom behavior

    for letter in string:
        quotient, remainder = divmod(entropy, len(generatedPassword))
        generatedPassword=(generatedPassword[:remainder] + letter + generatedPassword[remainder:])

        entropy = quotient
    return generatedPassword

def getOneCharPerRule(entropy, rules, exclude=""):
    getOneCharPerRule = ""
    for rule in rules:
        remainingChars = removeExcludedChars(CHARACTER_SUBSETS[rule], exclude)
        value, entropy = consumeEntropy("", entropy, remainingChars, 1)
        getOneCharPerRule += value
    return [getOneCharPerRule, entropy]

def getRules(passDetails):
    rules = ["lowercase", "uppercase", "digits", "symbols"]
    return [rule for rule in rules if rule in passDetails["rules"] and passDetails["rules"]]


def presentPassword(entropy, passDetails):
    rules = getRules(passDetails)
    excludedChars = (passDetails["exclude"] if "exclude" in passDetails else "")

    characterSet = getCharacters(rules, excludedChars)

    password, passwordEntropy = consumeEntropy("", entropy, characterSet, int(passDetails["length"])-len(rules))

    remainingCharacters, characterEntropy = getOneCharPerRule(passwordEntropy, rules, excludedChars)

    return insertStringPseudoRandomly(password, characterEntropy, remainingCharacters)

def makePassword(masterPassword, passDetails):
    entropy = calcEntropy(passDetails, masterPassword)
    return presentPassword(entropy, passDetails)


#print(removeExcludedChars("j^%pC*3UKDgzBr%lXMHqC", "j^%pC*3UKD"))


passDetails = {
    "site"  : "pbsKids",
    "login" : "SriLikesThatCake",
    #lowercase, uppercase, digits, symbols
    "rules" : ["lowercase", "digits", "symbols"],
    "exclude" : "j^%pC*3UKD",
    "length" : 15
}
'''
print(makePassword("j^%pC*3UKDgzBr%lXMHqC", passDetails))
print("PASSWORD")
#print(getRules(passDetails))


#print(calcEntropy(passDetails,"j^%pC*3UKDgzBr%lXMHqC" ))

var = calcEntropy(passDetails,"j^%pC*3UKDgzBr%lXMHqC")

#print(consumeEntropy("", var, getCharacters(), int(passDetails["length"])))
'''

def main():
    end = False

    while(end==False):

        print("1: generate a new master password")
        print("2: login")
        print("3: quit")

        mainMenu = input("enter prefered number to proceed.")
        if mainMenu == str(2):
            passDetails = {}
            options = ["site", "login", "rules", "exclude", "length"]

            index = 0

            while index <= 4:
                details = input(f"Enter {options[index]} details")
                if index == 3 and details == "none":
                    passDetails[options[index]] = ""
                    index+=1
                    continue
                if details == 'quit':
                    break

                passDetails[options[index]] = details
                index+=1

            print(passDetails)
            masterPassword = input("enter master password")


            print(makePassword(masterPassword, passDetails))
        elif mainMenu == str(3):
            print("exiting....")
            break
        elif mainMenu == str(1):
            print("PASSWORD")
            len = input("specify length of password")
            #length of string is 94 characters long
            SYMBOLS = CHARACTER_SUBSETS["lowercase"]+CHARACTER_SUBSETS["uppercase"]+CHARACTER_SUBSETS["digits"]+CHARACTER_SUBSETS["symbols"]
            masterPassword= ""
            for character in range(int(len)):
                num = int(quantumrandom.randint(0, 94))
                masterPassword+=SYMBOLS[num]

            passDetails = {
                "site"  : "37L>,5k*R?y`unyS",
                "login" : "}237'Ue`-.R_zc",
                #lowercase, uppercase, digits, symbols
                "rules" : ["lowercase", "uppercase", "digits", "symbols"],
                "exclude" : "",
                "length" : len
            }
            print("write this password down somewhere safe and cozy, we do not reccoment you storing this anywhere but in real life!")
            print(makePassword(masterPassword, passDetails))


    passDetails = {
        "site"  : "pbsKids",
        "login" : "SriLikesThatCake",
        #lowercase, uppercase, digits, symbols
        "rules" : ["lowercase", "digits", "symbols"],
        "exclude" : "j^%pC*3UKD",
        "length" : 15
    }

    print("generated password", " ", makePassword("j^%pC*3UKDgzBr%lXMHqC", passDetails))






if __name__ == '__main__':
    main()
