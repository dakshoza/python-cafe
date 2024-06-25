# How to run:
1. Install the requirements by running the code:
   `pip install -r requirements.txt`
2. Run the python file by running the code:
   `python biscotti_cafe_daksh_oza.py`


# About the code:

This Python program is designed to handle everything from taking orders to generating bills, just like a real cafe experience.

_Menu and Items_

First off, I defined the menu items using an enumeration (FoodItem). This helps in neatly categorizing each item like Coffee, Tea, Sandwich, Burger, Fries, and Cake. For each item, I also specified its price and preparation time using a data class (MenuItem). This makes it easy to update or add new items in the future.

_Orders and Tables_

The cafe has 6 tables, so I set up a system to manage orders for each table. Each order (Order) keeps track of the table number, items ordered with quantities (OrderItem), total bill, tip amount, and timestamps for entry and exit times.

_Interaction Flow_

When a waiter starts a new session, they can:
- Place an Order: This lets them choose a table and select items from the menu. The system calculates an approximate wait time based on the preparation times of the selected items.
- Add to Existing Order: If a table already has an active order, they can add more items to it.
- Close Order and Generate Bill: Once the customer is done, the waiter can close the order, calculate the total bill (including an optional tip), and store the order details.
- Exit: Simulates shutting down the store or ending the work day. Closes all open orders, saves order history, and displays session history.

_User Interface_

I've set up a user-friendly interface using a menu system:
- It prompts the waiter to choose an action (like placing an order or closing one).
- It validates inputs to ensure correct table numbers and item selections, handling errors gracefully.

_Data Handling_

To keep track of orders and history, I used Pandas DataFrames:
- Order History: Stores all orders across sessions in a CSV file (customer_data.csv), which is loaded at the start of each session.
- Session History: Keeps track of orders within the current session, which is updated and appended to the order history when closing orders.

_Special Features_

- Recommendations: Based on past orders, the system provides recommendations for popular dishes. It's a nice touch to enhance customer experience.
- Dynamic Menu Display: When placing orders, the menu is displayed with prices and preparation times, ensuring clarity for both customers and waitstaff.

Overall, the code is structured to mimic a real cafe's order system while being scalable for future expansions (like handling multiple orders or tables). It's designed with object-oriented principles and Pythonic practices, ensuring it's easy to maintain and extend.
