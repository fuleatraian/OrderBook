#Traian Fulea
#OrderBook Assessment

import csv
import Classes, Functions, DBObject, Order_Generator
from datetime import date
import datetime


# This code block interacts with the user, giving him ability to login/register on the trading platform. If the user is registering, the User.csv file will automatically update.
while True:
    Classes.ShowMessage().show_message("Please select whether you would like to login or register:")
    Classes.ShowMessage().show_message("1. Login")
    Classes.ShowMessage().show_message("2. Register")

    try:                 # We allow the user to introduce either option 1 or 2. If anything else is introduced, a friendly error is raised and tells him why it is not accepted.
        selection = int(input())

        #If a new user wants to register, it will be verified if its email address is a valid Gmail account.
        if selection == 2:            
            user = Classes.User()
            Classes.ShowMessage().show_message("Please introduce your email address. You need a valid Gmail address.")
            useremail = input()
            user.set_email(useremail)
            

            if Functions.validation(useremail) == True:
                userpassword = input()
                user.set_password(userpassword)
                Functions.register(DBObject.userdb, user.email, user.password)       # If user has a valid Gmail address, the database will be updated.
            
            else:
                Classes.ShowMessage().show_message("Please insert a valid Gmail address.")


        #If user wants to log in, it will be asked to introduce his email address and password.
        elif selection == 1:            
            Classes.ShowMessage().show_message("Please introduce your email address")
            Classes.ShowMessage().show_message("Email:")
            useremail = input()
            Classes.ShowMessage().show_message("Password:")
            userpassword = input()
            user = Classes.User(useremail, userpassword)


            if Functions.login(DBObject.userdb, user) == "Denied":          # If user's inputs do not match the records, it will be prompted that his email or password are incorrect, or he is not registered in the system.
                Classes.ShowMessage().show_message("Email or Password incorrect or non-existent. Please register or try again")

            elif Functions.login(DBObject.userdb, user) == "CLIENT":        # If the user's inputs match the records, it will be granted access but his rights depend on the authority he/she possesses
                Classes.ShowMessage().show_message("Authentication successful. You signed in as CLIENT")
                break

            else:
                Classes.ShowMessage().show_message("Authentication successful. You signed in as ADMIN")
                Classes.ShowMessage().show_message("You have full access. \n")
                break


        else:
            raise ValueError

    except ValueError:
        Classes.ShowMessage().show_message("You cannot introduce words, characters or other numbers except for options 1 or 2. \n")





while True:
    try:
        Classes.ShowMessage().show_message("Please choose from one of the following: \n 1.Place an order \n 2.Cancel your order \n 3.Replace your order \n 4.Display all orders \n 5. Display your own orders \n 6. Exit")
        selection = int(input())


        # With this block of code, the user is able to visualise all the public orders, being able to filter the results depending on preferences
        if selection == 4:
            Classes.ShowMessage().show_message("Please insert the order type you wish to show. If you want both BUY and SELL, please type 'All'")
            ordertype = input()
            intentionlist = Functions.orderintention(DBObject.orderdb, ordertype)
            Classes.ShowMessage().show_message("Please insert the stock you wish to show. If you want to see all stock, please type 'All'")
            stock = input()
            orderlist = Functions.orderstock(intentionlist, stock)
            Classes.ShowMessage().show_message(Functions.displayorder(orderlist))


        # This allows the user to add a new order to an order book
        elif selection == 1:
            Classes.ShowMessage().show_message("Please insert the stock you would like to post the order for")
            stock = input()
            book = Classes.OrderBook(stock)
            email = user.email
            Classes.ShowMessage().show_message("Please insert the quantity you want to trade")
            quantity = int(input())
            Classes.ShowMessage().show_message("Please specifiy the price you want to make the trade")
            price = int(input())
            Classes.ShowMessage().show_message("Lastly, please specify your intention to BUY or SELL")
            intention = input()
            book.newOrder(email, stock, quantity, price, intention)


        # This allows the user to cancel only his own orders from an order book
        elif selection == 2:
            Classes.ShowMessage().show_message("Please insert the id of the order you wish to delete.")
            id = input()
            Classes.ShowMessage().show_message("Please also delete the stock from which the order was initially for.")
            stock = input()
            book = Classes.OrderBook(stock)
            if id in Functions.personal_orders(user.email):
                book.cancelOrder(id)
            else:
                Classes.ShowMessage().show_message("You are not allowed to cancel this order because it is not yours")


        # This allows the user to replace one of his existing orders with a new one
        elif selection == 3:
            Classes.ShowMessage().show_message("Please select the id of the order you want to replace and its stock.")
            id = input()
            stock = input()
            book = Classes.OrderBook(stock)
            if id in Functions.personal_orders(user.email):
                Classes.ShowMessage().show_message("Please insert below the new order details. Please insert the stock of your order")
                stock = input()
                Classes.ShowMessage().show_message("Please insert the quantity of your order")
                quantity = int(input())
                Classes.ShowMessage().show_message("Please insert the price of your order")
                price = int(input())
                Classes.ShowMessage().show_message("Lastly, please insert whether you want to BUY or SELL")
                intention = input()
                new_id = id
                neword = Classes.Order(id = new_id, email = user.email, stock = stock, quantity = quantity, price = price, intention = intention, status = "Available", date = date.today())
                book.replaceOrder(id, neword)
            else:
                Classes.ShowMessage().show_message("You are not allowed to cancel this order because it is not yours")

        # This allows the user to display only his own orders
        elif selection == 5:
            print(Functions.display_userorders(user.email))


        elif selection == 6:
            print("Thank you for using our service. See you next time.")
            break

        else:
            raise ValueError
    except ValueError:
        print("Choose a valid option.")
    
# Finally, once a user is not using the platform anymore, we can show what happens behind the scenes
ordertrades = Classes.SORT(Order_Generator.stock)


# This method sorts ascendingly all the orders within all the orderbooks. We will demonstrate only for one order book
Classes.ShowMessage().show_message("Here are the sorted orders for one stock \n")
ordertrades.SortOrders()
print(ordertrades.orderBooks[1].show_status())


# This method returns single matches and we also test to check if the prices respect the conditions
singlematches = ordertrades.SingleMatch()

Classes.ShowMessage().show_message("Here are a couple matches found")
print(singlematches[0][0].id, singlematches[0][0].price, singlematches[0][1].price)
print(singlematches[1][0].id, singlematches[1][0].price, singlematches[1][1].price)
print(singlematches[2][0].id, singlematches[2][0].price, singlematches[2][1].price)


# This method returns all possible matches for each BUY order for each stock. The following for loop is just for verification
multimatches = ordertrades.MultipleMatch()

Classes.ShowMessage().show_message("Here are the multiple matches found for only one buy order")
print(multimatches[0][0].id, multimatches[0][0].price, multimatches[0][0].stock, multimatches[0][0].quantity, multimatches[0][0].intention)
for i in range(len(multimatches[1][1])):
    print(multimatches[1][1][i].id, multimatches[1][1][i].price, multimatches[1][1][i].stock, multimatches[1][1][i].quantity, multimatches[1][1][i].intention)


# Lastly, we can print out the trade history using this method. The following method can be used to update an already existing history with the trades executed today
Classes.ShowMessage().show_message("Here are the executed trades \n")

print(ordertrades.executeTrade())


print("\n")

Classes.ShowMessage().show_message("Here is the updated history of trades. \n")
print(ordertrades.update_TradeHistory([[11111, 22222, "TSLA", 500, 2500, 400, datetime.date(2020, 5, 17)]]))

"Here we will update the database following the execution of the trades"
ordertrades.updateOrderBooks()