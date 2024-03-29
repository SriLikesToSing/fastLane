import hashlib
import click
import requests


print("""


                                                          ,--,                                           
                                                       ,---.'|                                           
        ,---,.                          ___            |   | :                                           
      ,'  .' |                        ,--.'|_          :   : |                                           
    ,---.'   |                        |  | :,'         |   ' :                     ,---,                 
    |   |   .'              .--.--.   :  : ' :         ;   ; '                 ,-+-. /  |                
    :   :  :    ,--.--.    /  /    '.;__,'  /          '   | |__   ,--.--.    ,--.'|'   |   ,---.        
    :   |  |-, /       \  |  :  /`./|  |   |           |   | :.'| /       \  |   |  ,"' |  /     \       
    |   :  ;/|.--.  .-. | |  :  ;_  :__,'| :           '   :    ;.--.  .-. | |   | /  | | /    /  |      
    |   |   .' \__\/: . .  \  \    `. '  : |__         |   |  ./  \__\/: . . |   | |  | |.    ' / |      
    '   :  '   ," .--.; |   `----.   \|  | '.'|        ;   : ;    ," .--.; | |   | |  |/ '   ;   /|      
    |   |  |  /  /  ,.  |  /  /`--'  /;  :    ;        |   ,/    /  /  ,.  | |   | |--'  '   |  / |___   
    |   :  \ ;  :   .'   \'--'.     / |  ,   /         '---'    ;  :   .'   \|   |/      |   :    /  .\  
    |   | ,' |  ,     .-./  `--'---'   ---`-'                   |  ,     .-./'---'        \   \  /\  ; | 
    `----'    `--`---'                                           `--`---'                  `----'  `--"  
                                                                                                         



    """)

CHARACTER_SUBSETS = {
    "lowercase":"abcdefghijklmnopqrstuvwxyz",
    "uppercase":"ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "digits":"0123456789",
    "symbols":"!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
}


def calcEntropy(passwordProfile, masterPassword):
    #salt is basically the cryptographic additions of bits you add to make the password more unique and secure before hashing.
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
    if passDetails["rules"] == '':
        return rules
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


def main():
    end = False

    while(end==False):
        print('\n')
        print("1: generate a new master password")
        print("2: login")
        print("3: quit")

        mainMenu = input("enter prefered number to proceed. ")
        if mainMenu == str(2):
            passDetails = {}
            options = ["site", "login", "rules", "exclude", "length"]

            index = 0

            while index <= 4:
                details = input(f"Enter {options[index]} details: ")
                if  index == 1:
                    print("type out each rule separated with comma's. If left blank it will use every rule")
                    print("Rules: lowercase, uppercase, digits, symbols")
                if index == 3 and details == "none":
                    passDetails[options[index]] = ""
                    index+=1
                    continue
                if details == 'quit':
                    break

                passDetails[options[index]] = details
                index+=1
            if passDetails[options[4]] == '':
                raise Exception("Please input the length for the password to retrieve it")

            masterPassword = input("enter master password ")


            print(makePassword(masterPassword, passDetails))
        elif mainMenu == str(3):
            print("exiting....")
            exit(0)
        elif mainMenu == str(1):
            len = input("specify length of password: ")
            try:
                int(len)
            except:
                print('\n')
                print("Sorry, please input integer")
                continue


            print("generating... this might take a while ") 
            #length of string is 94 characters long
            SYMBOLS = CHARACTER_SUBSETS["lowercase"]+CHARACTER_SUBSETS["uppercase"]+CHARACTER_SUBSETS["digits"]+CHARACTER_SUBSETS["symbols"]
            masterPassword= ""
            for character in range(int(len)):
                source = "https://www.random.org/integers/?num=1&min=1&max=93&col=5&base=10&format=plain&rnd=new"
                num = requests.get(source)
                num= int(num.text)

                masterPassword+=SYMBOLS[num]

            passDetails = {
                "site"  : "37L>,5k*R?y`unyS",
                "login" : "}237'Ue`-.R_zc",
                #lowercase, uppercase, digits, symbols
                "rules" : ["lowercase", "uppercase", "digits", "symbols"],
                "exclude" : "",
                "length" : len
            }
            print('\n')
            print("write this password down somewhere safe and cozy, we do not reccomend you storing this anywhere but in real life!")
            print(makePassword(masterPassword, passDetails))


if __name__ == '__main__':
    main()
