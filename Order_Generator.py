
import random
import csv
from datetime import datetime


# Create a function to return a randomly created share price
def shareprice():
    return round(random.randint(500, 1000))



# Create a function to return a randomly generated quantity
def quantity():
    return random.randint(1, 100)



# Create a function to return a randomly generated date within January 2022
def datepost():
    return datetime(year = 2022,  month = 1, day = random.randint(1, 31)).date()



# Create a function that reads all the user emails from the User.csv file and stores them in a list, so we can later pick an email randomly
def reademail():
    userfile = open("D:/Albany Beck/Python Training/Assessments/Module 1/User.csv", "r")
    userreader = csv.reader(userfile)
    header = next(userreader)
    useremail = list()
    for row in userreader:
        useremail.append(row[0])
    userfile.close()
    return useremail



# This function uses a list of the data with all the orders' information provided and it will populate the Order.csv file
def generateorders(data):
    with open("D:/Albany Beck/Python Training/Assessments/Module 1/Order.csv", "w", newline="") as userfile:
        userwriter = csv.writer(userfile)
        userwriter.writerows(data)


# Manually introduce 30 companies' names
stock = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA', 'FB', 'TSM', 'NVDA', 'JNJ', 'JPM', 'UNH', 'BAC', 'WMT', 'MA', 'BABA', 'PFE', 'TM', 'DIS', 'KO', 'ADBE', 'PEP', 'NKE', 'NFLX', 'ORCL', 'INTC', 'COST', 'PYPL', 'AZN', 'UPS', 'HSBC']


"""

The following code generates random numbers of buy and sell orders for each stock, making sure that we have a total of 500 sell orders and 500 buy orders.
It is worth mentioning that this process produce at least one BUY and at least one SELL order for each company, but it is rather slow. Therefore, we will allow some companies to not have shares at all

while True:
  buyorders = [random.randint(1, 20) for i in range(len(stock))]
  if sum(buyorders) == 500:
    break

while True:
  sellorders = [random.randint(1, 20) for i in range(len(stock))]
  if sum(sellorders) == 500:
    break

print(buyorders)
print(sellorders)


"""

# Store all the user emails into the useremail list
useremail = reademail()

# Now we will add orders. It is important to keep track of the order numbers, so we end up with exactly 500 BUY orders and 500 SELL orders.
usedid = list(range(1000))
buyord = 500
sellord = 500
orderdata = [["ID", "Email", "Stock", "Quantity", "Price", "Intention", "Status", "Date"]]


for i in range(1000):

    # We do not allow to have duplicate order ID's
    id = random.choice(usedid)
    usedid.remove(id)

    # Pick email and stock randomly from the lists created and also generate random number of shares, share price and date when the order has been placed.
    email = random.choice(useremail)
    company = random.choice(stock)
    quant = quantity()
    price = shareprice()
    status = random.choice(["FULLY FILLED", "PARTIALLY FILLED", "AVAILABLE"])            # We also considered all available orders as NEW ORDER
    time = datepost()

    # We make sure that we respect the number of SELL and BUY orders
    if buyord > 0 and sellord > 0:
        intention = random.choice(["BUY", "SELL"])
        if intention == "BUY":
            buyord -= 1
        else:
            sellord -= 1

    elif buyord == 0:
        intention = "SELL"
        sellord -= 1

    else:
        intention = "BUY"
        buyord -= 1
    
    orderdata.append([id, email, company, quant, price, intention, status, time])
    

#Now calling the function generateorders will create our Order.csv file
generateorders(orderdata)
