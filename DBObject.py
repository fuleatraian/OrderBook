#Traian Fulea


import csv
import Classes


# Read the initial user details from the csv file and store them in a list. Users are stored as objects into a list (adapted from https://www.analyticsvidhya.com/blog/2021/08/python-tutorial-working-with-csv-file-for-data-science/)
#This piece of code was adapted from 
userdb = list()
userfile = open("D:/Albany Beck/Python Training/Assessments/Module 1/User.csv")
usercsv = csv.reader(userfile)
userheader = next(usercsv)
for row in usercsv:
    userdb.append(Classes.User(row[0], row[1], row[2]))
userfile.close()




# Read the initial order details from the csv file and store them in a list. Orders are stored as objects into a list (adapted from https://www.analyticsvidhya.com/blog/2021/08/python-tutorial-working-with-csv-file-for-data-science/)
orderdb = list()
orderfile = open("D:/Albany Beck/Python Training/Assessments/Module 1/Order.csv")
ordercsv = csv.reader(orderfile)
orderheader = next(ordercsv)
for row in ordercsv:
    orderdb.append(Classes.Order(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
orderfile.close()


