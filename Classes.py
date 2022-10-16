#Traian Fulea


import csv, random
from email.message import Message
from datetime import date
import Functions, Order_Generator

#Create a class to display any message needed, so we avoid using print() statement
class ShowMessage:
    def __init__(self, message = None):
        self.message = message

    def get_message(self):
        return self.message

    def show_message(self, new_message):
        self.message = new_message
        print(self.message)



# Create a User class so we can easily access its email, password and authority
class User:
    def __init__(self, email = None, password = None, authority = "CLIENT"):               # Here data takes default value None but it represents a nested list containing all the details of an order/user
        self.email = email
        self.password = password
        self.authority = authority

    def set_email(self, new_email):
        self.email = new_email

    def set_authority(self, new_authority):
        self.authority = new_authority
        
    def set_password(self, new_password):          # Allow user to set/reset its password
        self.password = new_password

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password



# Create an Order class so we can easily access its details
class Order:
    def __init__(self, id, email, stock, quantity, price, intention, status = "Available", date = date.today()):
        self.id = int(id)
        self.email = email
        self.stock = stock
        self.quantity = int(quantity)
        self.price = int(price)
        self.intention = intention
        self.status = status
        self.date = date

    def set_status(self, status):       # Here we allow each order status to be changed
        self.status = status

    def set_quantity(self, quantity):       # Here we allow each order quantity to be changed (following an exchange)
        self.quantity = quantity




# Create an OrderBook class, so we can store all the orders of the same stock in the same OrderBook object
class OrderBook(Order):
    def __init__(self, stock):
        self.stock = stock
        orderbook= list()
        orderfile = open("D:/Albany Beck/Python Training/Assessments/Module 1/Order.csv")
        ordercsv = csv.reader(orderfile)
        next(ordercsv)
        for row in ordercsv:
            if row[2] == stock:
                orderbook.append(Order(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        orderfile.close()

        self.orders = orderbook


    # This method adds a new order to the orderbook
    def newOrder(self, email, stock, quantity, price, intention, id =  random.randint(1000, 10000), status = "AVAILABLE", date = date.today()):
        self.orders.append(Order(id, email, stock, quantity, price, intention, status, date))
        row = [id, email, stock, quantity, price, intention, status, date]
        Functions.updatecsv("D:/Albany Beck/Python Training/Assessments/Module 1/Order.csv", row)
        ShowMessage().show_message("Order added succesfully and assigned id: {}".format(id))
        return self.orders


    # This method removes an existing method from the orderbook
    def cancelOrder(self, id):
        row = [i for i in self.orders if i.id == int(id)]
        self.orders.remove(row[0])
        header = ["ID", "Email", "Stock", "Quantity", "Price", "Intention", "Status", "Date"]
        Functions.deleterow("D:/Albany Beck/Python Training/Assessments/Module 1/Order.csv", header, row[0].id)
        ShowMessage().show_message("Order id {} removed succesfully.".format(id))
        return self.orders


    # Using this method, the client can replace an order by cancelling the first order and adding a new one. The parameter id is given by the id of the order which need to be replaced
    def replaceOrder(self, id, ordertwo):
        self.cancelOrder(id)
        self.newOrder(ordertwo.email, ordertwo.stock, ordertwo.quantity, ordertwo.price, ordertwo.intention)
        return self.orders


    # This method returns the status of all the orders within the orderbook, alongside some minimal information
    def show_status(self):
        orderstatus = list()
        for order in self.orders:
            orderstatus.append([order.stock, order.quantity, order.price, order.status])
        return orderstatus
    


class Exchange(OrderBook):
    def __init__(self):
        self.feeLadder = 0
        self.todaysTradeValue = 0

    def set_fee(self, feeLadder):
        self.feeLadder = feeLadder

    def set_todaysTradeValue(self, todayTradeValue):
        self.todaysTradeValue = todayTradeValue

    def get_fee(self):
        return self.feeLadder
    
    def get_todayTradeValue(self):
        return self.todaysTradeValue


class SORT(Exchange, OrderBook):
    def __init__(self, stocks):
        orderbooks = list()
        for stock in stocks:
            orderbooks.append(OrderBook(stock))   # This groups together all the orderbooks and stores them in a new SORT object
        self.exchanges = []
        self.orderBooks = orderbooks


    # This method does not return an output but it sorts ascendingly all the orders within every orderbook object
    def SortOrders(self):
        for book in self.orderBooks:
            book.orders.sort(key = lambda obj: int(obj.price))


    # This method returns all buy orders, partially filled or available within a specific stock
    def get_buyorders(self, stock):
        buy_orders = []
        book = OrderBook(stock)
        book.orders.sort(key = lambda obj: int(obj.price))
        for i in range(len(book.orders)):
            if book.orders[i].intention == "BUY" and book.orders[i].status in ["PARTIALLY FILLED", "AVAILABLE"]:
                buy_orders.append(book.orders[i])
                buy_orders.reverse()      # We reverse this particular list because we want the maximum BUY orders to be indexed first in the list
        return buy_orders


    # This method returns all sell orders, partially filled or available within a specific stock
    def get_sellorders(self, stock):
        sell_orders = []
        book = OrderBook(stock)
        book.orders.sort(key = lambda obj: int(obj.price))
        for i in range(len(book.orders)):          
                if book.orders[i].intention == "SELL" and book.orders[i].status in ["PARTIALLY FILLED", "AVAILABLE"]:
                    sell_orders.append(book.orders[i])
        return sell_orders


    # This method returns a single match for every order within an orderbook, matching the highest buy price with the lowest sell price for each stock
    def SingleMatch(self):
        single_matches = []
        for stock in Order_Generator.stock:
            buy_orders = self.get_buyorders(stock)
            sell_orders = self.get_sellorders(stock)
            for i in range(len(buy_orders)):            # Now we iterate over the two lists and select one match and append it to single_matches list, if the difference between the buy and sell price are within a threshold of 5%
                count = 0
                for j in range(len(sell_orders)):
                    if buy_orders[i].price > sell_orders[j].price:
                        single_matches.append([buy_orders[i], sell_orders[j]])
                        count += 1
                    if count == 1:      # Here we make sure that we try to match every buy order with only one sell order
                        break
        return single_matches


    # This method is similar with the single matches but this time we allow multiple matches
    def MultipleMatch(self):
        multiple_matches = []
        for stock in Order_Generator.stock:
            buy_orders = self.get_buyorders(stock)
            sell_orders = self.get_sellorders(stock)
            for i in range(len(buy_orders)):            
                potential_matches = []          # The potential matches list is gathering all the sell potential matches that the buyer could be matched with
                for j in range(len(sell_orders)):
                    if buy_orders[i].price > sell_orders[j].price:
                        potential_matches.append(sell_orders[j])    
                multiple_matches.append([buy_orders[i], potential_matches])
        return multiple_matches


    # This method would execute the trades, establish the fees of the trade and also the total value of trades happened today
    def executeTrade(self):
        trade = []
        for match in self.MultipleMatch():                                      # First we iterate over each multiple match and execute trades of the buy order to the sell orders available, which are already ordered                                         
            if len(match[1]) > 0:                         #We want to make sure that we apply this process only if there is at least one match with our order
                for i in range(len(match[1])):                                  # As long as the quantity of the buy order is higher than 0, means that potentially another trade is possible, if any matched sell order is still available  
                    if match[0].quantity > 0 and match[0].status != "FULLY FILLED":                                             
                        tradequantity = min(match[0].quantity, match[1][i].quantity)              # We first calculate the fees of the trade, depending on the quantity traded
                        
                        if tradequantity < 10:
                            fee = 0.5 * match[0].price
                        elif tradequantity >= 10 and tradequantity < 100:
                            fee = 0.3 * match[0].price
                        elif tradequantity >= 100 and tradequantity <1000:
                            fee = 0.1 * match[0].price
                        else:
                            fee = 0.01 * match[0].price

                        if match[0].quantity == tradequantity:                  # Update both the seller and buyer quantities post trade and record the details of the trade into a new list
                            match[0].set_status("FULLY FILLED")
                            remainder = match[1][i].quantity - tradequantity
                            match[1][i].set_quantity(remainder)
                            match[1][i].set_status("PARTIALLY FILLED")
                        else:
                            match[1][i].set_status("FULLY FILLED")
                            remainder = match[0].quantity - tradequantity
                            match[0].set_quantity(remainder)
                        
                        exchange = Exchange()
                        exchange.set_fee(fee)
                        if tradequantity == 0:
                            pass
                        else:
                            trade.append([match[0].id, match[1][i].id, match[0].stock, tradequantity, match[0].price, round(exchange.feeLadder,2), date.today()])
        todaysTradeValue = sum(element[4] for element in trade)
        exchange.set_todaysTradeValue(todaysTradeValue)
        return trade

    # This method builds or updates an existing trade history record
    def update_TradeHistory(self, tradehistory):
        newtrades = self.executeTrade()
        tradehistory.extend(newtrades)
        Functions.makecsv("D:/Albany Beck/Python Training/Assessments/Module 1/Trade History.csv", ["From", "To", "Stock", "Quantity", "Price", "Fees", "Date"], tradehistory)
        return tradehistory


    # This method executes trades but in the same time updates the database. The update was possible using the commented lines of code. However, for visualisation ease, we created a sperated file called "Updated Orders.csv" to show the status of the orders post trade execution
    def updateOrderBooks(self):
        pretrade = Functions.read_orders()
        trade = self.executeTrade()
        row = list()
        for order in pretrade:
            for exchange in trade:
                if order.id == exchange[0] or order.id == exchange[1]:
                    if order.quantity == exchange[3]:             
                        order.set_status("FULLY FILLED")
                    else:
                        remained = order.quantity - exchange[3]
                        order.set_quantity(remained)
                        order.set_status("PARTIALLY FILLED")
            row.append([order.id, order.email, order.stock, order.quantity, order.price, order.intention, order.status, order.date])
        Functions.makecsv("D:/Albany Beck/Python Training/Assessments/Module 1/Updated Orders.csv", ["ID", "Email", "Stock", "Quantity", "Price", "Intention", "Status", "Date"], row)
                    # OrderBook(order.stock).cancelOrder(order.id)
                    # OrderBook(order.stock).newOrder(id = order.id, email = order.email, stock = order.stock, quantity = order.quantity, price = order.price, intention = order.intention, status = order.status, date = order.date)



#-----------------------------Different Attempts---------------------------------------------------------------------



# # This method would execute the trades, establish the fees of the trade and also the total value of trades happened today
#     def executeTrade(self):
#         trade = []
#         for match in self.MultipleMatch():                                      # First we iterate over each multiple match and execute trades of the buy order to the sell orders available, which are already ordered                             
#             while match[0].quantity > 0:                                        # As long as the quantity of the buy order is higher than 0, means that potentially another trade is possible, if any matched sell order is still available
#                 for i in range(len(match[1])):                                               
#                     tradequantity = min(match[0].quantity, match[1][i].quantity)              # We first calculate the fees of the trade, depending on the quantity traded
                    
#                     if tradequantity < 10:
#                         fee = 0.5 * match[0].price
#                     elif tradequantity >= 10 and tradequantity < 100:
#                         fee = 0.3 * match[0].price
#                     elif tradequantity >=100 and tradequantity <1000:
#                         fee = 0.1 * match[0].price
#                     else:
#                         fee = 0.01 * match[0].price

#                     if match[0].quantity == tradequantity:                  # Update both the seller and buyer quantities post trade and record the details of the trade into a new list
#                         match[0].set_status("FULLY FILLED")
#                         match[1][i].set_quantity(match[1][i].quantity - tradequantity)
#                         match[1][i].set_status("PARTIALLY FILLED")
#                     else:
#                         match[1][i].set_status("FULLY FILLED")
#                         match[0].set_quantity(match[0].quantity - tradequantity)
                    

#                     exchange = Exchange()
#                     exchange.set_fee(fee)
#                     trade.append([match[0].id, match[1][i].id, match[0].stock, tradequantity, match[0].price, exchange.feeLadder, date.today()])
#         return trade



    """ This method was firstly created but then was broken down into 3 distinct methods for code reusability"""
    # def SingleMatches(self):
    #     single_matches = []
    #     buy_orders = []
    #     sell_orders = []
    #     for book in self.orderBooks:
    #         book.orders.sort(key = lambda obj: int(obj.price))
    #         for i in range(len(book.orders)):
    #             if book.orders[i].intention == "BUY" and book.orders[i].status in ["PARTIALLY FILLED", "AVAILABLE"]:
    #                 buy_orders.append(book.orders[i])
    #                 buy_orders.reverse()      # We reverse this particular list because we want the maximum BUY orders to be indexed first in the list
    #         for i in range(len(book.orders)):          
    #             if book.orders[i].intention == "SELL" and book.orders[i].status in ["PARTIALLY FILLED", "AVAILABLE"]:
    #                 sell_orders.append(book.orders[i])
    #         for i in range(len(buy_orders)):            # Now we iterate over the two lists and select one match and append it to single_matches list, if the difference between the buy and sell price are within a threshold of 5%
    #             count = 0
    #             for j in range(len(sell_orders)):
    #                 if (buy_orders[i].price >= sell_orders[j].price * 95 / 100) and (buy_orders[i].price <= sell_orders[j].price * 105 / 100):
    #                     single_matches.append([buy_orders[i], sell_orders[j]])
    #                     count += 1
    #                 if count == 1:      # Here we make sure that we try to match every buy order with only one sell order
    #                     break
    #     return single_matches

    