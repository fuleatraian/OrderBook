#Traian Fulea
#This piece of code will help to generating  passwords

import random
import csv

#Function that generates a random email address
def new_user():     
    char = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890")   
    user = "".join(random.choice(char) for i in range(10))
    return user + "@gmail.com"

#Function that generates a random password
def new_password():
    char = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890")   
    password = "".join(random.choice(char) for i in range(10))
    return password

#Now we will generate 300 users, alongside their emails and passowrds
userdata = list()
for i in range(300):
    email = new_user()
    password = new_password()
    authority = "CLIENT"
    userdata.append([email, password, authority])

#Now we will write the data for each user as a new row in the User.csv file. We use "a" because we want to append rows to the existing rows in the file. Prior completing this step, ADMIN users were added manually. (Adapted from https://stackoverflow.com/questions/2363731/append-new-row-to-old-csv-file-python)
with open("D:/Albany Beck/Python Training/Assessments/Module 1/User.csv", "a", newline="") as userfile:
    userwriter = csv.writer(userfile)
    userwriter.writerows(userdata)


