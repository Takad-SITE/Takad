# ----- validation and authentication -----

import bcrypt # for hasing and salt
import re # for Regular Expressions

#___________________________________________________________________

# --------- NEVER change any variable's value in this file ---------
#___________________________________________________________________

# this is a secret value for password which will use it in hashing process
# Warning  change this value will ifect old user can not login , becuase thier passowrd will not match
pepperForPasswords ="p[j*u$+v(r*0_}A" 

#__________________________ functions __________________________

#tis function return strong hashed password  to stor it in DB 
def hashThisPassowrdForDB(theRealPasswodOfUser):
    # pepperForPasswords is extra value for applying more security
    passwrdWithPupper = pepperForPasswords+theRealPasswodOfUser
    # created  hashed password but not ready "" inculded   " b' "
    hashedPassword_NotReady = bcrypt.hashpw(passwrdWithPupper.encode(),bcrypt.gensalt()) # gen hashing with salt
    #for removing the " b' " and make it read to story it in the DB
    return hashedPassword_NotReady.decode() # the passsowrd now ready to stor in DB

#this function for check hashed password in DP and the real passowrd ( as inpute from User)
#this function will return true \ false
def checkPassowrd(theRealPasswodOfUser, hashedPasswordFromDB):
    passwrdWithPupper = pepperForPasswords+theRealPasswodOfUser
    
    return bcrypt.checkpw(passwrdWithPupper.encode(), hashedPasswordFromDB.encode()) #True\False

def isVeryStrongPassword(inputPassword):
    # ^((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,})$

    #(?=.*\d)        #   must contain at least one digit
    #(?=.*[a-z])     #   must contain at least one lowerrcase character
    #(?=.*[A-Z])     #   must contain at least one uppercase character
    #(?=.*\W)        #   must contain at least one special symbol
    #{8,}            #   length at least 8 characters

    #length minimum 8 characters at least one digit, lowerrcase, uppercase, and special.
    patternVeryStrongPassword = re.compile("^((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,})$")

    return bool(patternVeryStrongPassword.match(inputPassword)) # if it's strong password return True othetwise return False

def isItValidName(inputName):
    # length at least 2 characters
    if len(inputName) <2 :
        return False
    # Expression can start only with a letter
    # Expression can contain letters or spaces
    patternName=re.compile("^[a-zA-z][a-zA-z\s]*$")  # ^[a-zA-z][a-zA-z\s]*$   ^([a-zA-z]{2,})$
    return bool(patternName.match(inputName)) # True/ False

def isItValidEmail (inputEmail):
    patternEmail= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    return bool(patternEmail.match(inputEmail)) # True / False
