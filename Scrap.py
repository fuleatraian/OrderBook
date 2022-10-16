
from dataclasses import replace
import random
import csv
from datetime import datetime, date
import DBObject, Order_Generator, Functions, Classes

#Read the users details and store them in a list


#Read the order details and store them in a list

# class User:
#     def __init__(self, email = None, password = None, authority = "CLIENT"):
#         self.email = email
#         self.password = password
#         self.authority = authority

#     def set_user(self, email):
#         self.email = email
#         return self.email

#     def set_password(self, password):
#         self.password = password
#         return self.password

#     def reset_password(self, new_password):
#         self.password = new_password
#         return self.password


# userdb = list()
# userfile = open("D:/Albany Beck/Python Training/Assessments/Module 1/User.csv")
# usercsv = csv.reader(userfile)
# header = next(usercsv)
# for row in usercsv:
#     userdb.append(User(row[0], row[1], row[2]))
# #print(userdb)
# for i in userdb:
#     print(i.email)
# userfile.close()

# def authentication(user):
#     if user.email not in db["User email"]:
#         print("Email address not recognized, please register.")
#         print("Please insert your email:")
#         user.set_user(input())
#         print("Please insert your password:")
#         user.set_password(input())

#     else:
#         print("User registered, please insert your password")
#         if user.password == d

# a = User()

# authentication(a)


# print(datetime(year = 2022,  month = 1, day = random.randint(1, 30)).date())


# print(random.choice(["BUY", "SELL"]))


# def orderintention(data, ordertype):
#     orderlist = list()
#     if ordertype in ["BUY", "SELL"]:
#         for obj in data:
#             if obj.intention == ordertype:
#                 orderlist.append(obj)
#     elif ordertype == "All":
#         return data
#     else:
#         print("Please select a valid intention (SELL/BUY/All).")
#     return orderlist



# def orderstock(data, stock):
#     orderlist = list()
#     if stock in Order_Generator.stock:
#         for obj in data:
#             if obj.stock == stock:
#                 orderlist.append(obj)
#     elif stock == "All":
#         return data
#     else:
#         print("The stock chosen does not exist in the system. Please choose a different stock.")
#     return orderlist


# intentionlist = orderintention(DBObject.orderdb, "BUY")
# orderlist = orderstock(intentionlist, "GOOG")

# # for obj in orderlist:
# #     print(obj.id, obj.stock, obj.intention)

# displaydata = Functions.displayorder(orderlist)

# Functions.makecsv("D:/Albany Beck/Python Training/Assessments/Module 1/Display_Orders.csv", ["ID", "Email", "Stock", "Quantity", "Price", "Intention", "Status", "Date"], displaydata)

# print(DBObject.userdb[1].email)



# intentionlist = []
# [intentionlist.append(obj.intention) for obj in DBObject.orderdb if obj.intention == "BUY"]
# print(intentionlist)

# def orderintention(data, ordertype = "All"):   
#     orderlist = list()
#     if ordertype in ["BUY", "SELL"]:
#         for obj in data:
#             if obj.intention == ordertype:
#                 orderlist.append(obj)
#     elif ordertype == "All":
#         return data
#     else:
#         print("Please select a valid intention (SELL/BUY/All).")
#     return orderlist


# def orderintention(data, intention):   
#     orderlist = list()
#     if intention in ["BUY", "SELL"]:
#         [orderlist.append(obj) for obj in data if obj.intention == intention]
#     elif intention == "All":
#         return data
#     else:
#         Classes.ShowMessage().show_message("Please select a valid intention (SELL/BUY/All).")
#     return vars(orderlist[2])


# print(orderintention(DBObject.orderdb, "BUY"))

# Create an Order class so we can easily access its detail

# intentionlist = Functions.orderintention(DBObject.orderdb, "All")
# orderlist = Functions.orderstock(intentionlist, "GOOG")

# print(orderlist)

# def func(id):
#     book = Classes.OrderBook("TSLA")
#     #print(len(book.orders))

#     book.newOrder(id = 6358, email = "neworderuser@gmail.com", stock = "GOOG", quantity = "10", price = "150", intention = "BUY")


#     #print(len(book.orders))

#     book.cancelOrder(id)



#orderone = Classes.Order(id = 6358, email = "neworderuser@gmail.com", stock = "GOOG", quantity = "10", price = "150", intention = "BUY")


#ordertwo = Classes.Order(id = 6500, email = "neworderuser2@gmail.com", stock = "GOOG", quantity = "100", price = "100", intention = "SELL")

#book.replaceOrder(orderone, ordertwo)

# print(len(book.orders))

# print(book.orders[-1].id)

# header = ["ID", "Email", "Stock", "Quantity", "Price", "Intention", "Status", "Date"]
# Functions.deleterow("D:/Albany Beck/Python Training/Assessments/Module 1/Order.csv", header, row[0].id)



#print(book.show_status())

# print(len(book.orders))

# Functions.sort(book.orders)

# for obj in book.orders:
#     print(obj.price)

books = Classes.SORT(Order_Generator.stock)

books.SortOrders()
print(books.orderBooks[1].show_status())

# print(book.orders[1].status in ["PARTIALLY FILLED", "AVAILABLE"])

# book.orders.sort(key = lambda obj: obj.price)
# print(book.orders)
sell_orders = []
# for i in range(len(book.orders)):           # We iterate from end to beginning because all orderbooks are sorted ascendingly and we want the highest sell orders to be the first ones in the sell_orders list
#     if book.orders[i].intention == "SELL" and book.orders[i].status in ["PARTIALLY FILLED", "AVAILABLE"]:
#         sell_orders.append(book.orders[i])
#         sell_orders = sell_orders.reverse

for i in sell_orders:
    print(i.price)

a = books.SingleMatch()
print(a[0][0].id, a[0][0].price, a[0][1].price)
print(a[1][0].id, a[1][0].price, a[1][1].price)
print(a[2][0].id, a[2][0].price, a[2][1].price)

b = books.MultipleMatch()

#print(b)

print(b[0][0].id, b[0][0].price, b[0][0].stock, b[0][0].quantity, b[0][0].intention)
for i in range(len(b[1][1])):
    print(b[1][1][i].id, b[1][1][i].price, b[1][1][i].stock, b[1][1][i].quantity, b[1][1][i].intention)



c = books.executeTrade()

d = books.update_TradeHistory(["hahahaha"])

print(d)

id = input()
print(Functions.stock_identifier(id))

row = [i for i in [[1,2],[3,4]] if i[0] == 1]
print(row)