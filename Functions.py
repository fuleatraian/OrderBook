#Traian Fulea


import csv
import Order_Generator, Classes



# This function writes a list to a csv file from scratch
def makecsv(filepath, header, rows):
    file = open(filepath, "w", newline = "")
    filewriter = csv.writer(file)
    filewriter.writerow(header)
    filewriter.writerows(rows)
    file.close()



# This function updates an already existing csv file
def updatecsv(filepath, row):
    file = open(filepath, "a", newline = "")
    filewriter = csv.writer(file)
    filewriter.writerow(row)
    file.close()



# This function deletes a specific row from a csv file and rewrites the file
def deleterow(filepath, header, id = None):
    lines = list()
    with open(filepath, "r") as file:
        filereader = csv.reader(file)
        next(filereader)
        [lines.append(row) for row in filereader if int(row[0]) != id]
    makecsv(filepath, header, lines)



# Function that iterates through emails in the database and checks if the given email is already recorded in the data
def iteremail(data, email):
    usage = False
    for i in range(len(data)):
        if email == data[i].email:
            usage = True
            break
    return usage


# Check if an email is a valid Gmail account
def validation(email):
    if email[-10:] == "@gmail.com":
        return True 
    else:
        return False



# The register function appends the new user's email and passwords to the User.csv file. By default, it registers the new user as CLIENT.
# If the new user is an admin, it will have to be manually introduced to the database or automatically added following some additional security requirements, which could be added, if needed.
def register(data, email, password, authority = "CLIENT"):
    if iteremail(data, email) == True:
        Classes.ShowMessage().show_message("Email address is already used.")        
    else:                                       # If the email is not registered in the system, it updates the User.csv file with the details of the new user.
        updatecsv("D:/Albany Beck/Python Training/Assessments/Module 1/User.csv", [email, password, authority])
        data.append(Classes.User(email, password, authority))



# Check if the login details of the user correspond with the database records, and if they do, reference user placeholder to the same user object in the memory. Function returns if the access was granted or not
def logincheck(data, user):
    access = False
    for i in range(len(data)):
        if user.email == data[i].email and user.password == data[i].password:         # If the user input email and password match the records, it is granted access.
            user.set_authority(data[i].authority)
            access = True
            break
        elif user.email != data[i].email or user.password != data[i].password:
            continue
    return access



# If the user's credentials match the database records, it logs him in and returns whether he is a CLIENT or ADMIN.
def login(data, user):           
    if logincheck(data, user) == False:
        return "Denied"
    else:
        return user.authority                # If access is granted, the function will return whether the user is a CLIENT or an ADMIN.




# This function filters the orders by the intention to BUY/SELL or just returns both BUY and SELL, depending on user preferences
def orderintention(data, intention):   
    orderlist = list()
    if intention in ["BUY", "SELL"]:
        [orderlist.append(obj) for obj in data if obj.intention == intention]
    elif intention == "All":
        return data
    else:
        Classes.ShowMessage().show_message("Please select a valid intention (SELL/BUY/All).")
    return orderlist



# This function filters the orders by stock chosen by the user, or simply displays all the orders regardless of the stock
def orderstock(data, stock):
    orderlist = list()
    if stock in Order_Generator.stock:
        [orderlist.append(obj) for obj in data if obj.stock == stock]
    elif stock == "All":
        return data
    else:
        Classes.ShowMessage().show_message("The stock chosen does not exist in the system. Please choose a different stock.")
    return orderlist



# This function iterates over a list of objects(orders) and returns them as nested list. Moreover, it writes the result to a csv file for a user to download and analyse.
def displayorder(orderlist):
    displaydata = list()
    if orderlist == []:
        return "No match found."
    else:
        for obj in orderlist:
            displaydata.append([obj.id, obj.email, obj.stock, obj.quantity, obj.price, obj.intention, obj.status, obj.date])
        makecsv("D:/Albany Beck/Python Training/Assessments/Module 1/Display_Orders.csv", ["ID", "Email", "Stock", "Quantity", "Price", "Intention", "Status", "Date"], displaydata)
        return displaydata


# This function takes as argument an email given by the user in the moment of login and restricts him from cancelling or modifying other orders, which are not his
def personal_orders(email):
    ordersid = []
    orderfile = open("D:/Albany Beck/Python Training/Assessments/Module 1/Order.csv")
    ordercsv = csv.reader(orderfile)
    orderheader = next(ordercsv)
    for row in ordercsv:
        if row[1] == email:
            ordersid.append(row[0])
    orderfile.close()
    return ordersid         



def display_userorders(email):
    orders = []
    orderfile = open("D:/Albany Beck/Python Training/Assessments/Module 1/Order.csv")
    ordercsv = csv.reader(orderfile)
    orderheader = next(ordercsv)
    for row in ordercsv:
        if row[1] == email:
            orders.append(row)
    orderfile.close()
    return orders  


def read_orders():
    orders = []
    orderfile = open("D:/Albany Beck/Python Training/Assessments/Module 1/Order.csv")
    ordercsv = csv.reader(orderfile)
    next(ordercsv)
    for row in ordercsv:
        orders.append(Classes.Order(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
    orderfile.close()
    return orders


            
