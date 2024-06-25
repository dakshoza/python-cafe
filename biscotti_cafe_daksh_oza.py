from typing import Dict, List
from dataclasses import dataclass, field
from enum import Enum, auto
import pandas as pd
from datetime import datetime
import os
from collections import Counter
import re
import math

class FoodItem(Enum):
    COFFEE = auto()
    TEA = auto()
    SANDWICH = auto()
    BURGER = auto()
    FRIES = auto()
    CAKE = auto()

@dataclass
class MenuItem:
    item: FoodItem
    price: float
    prep_time: int  # in minutes

@dataclass
class OrderItem:
    item: FoodItem
    quantity: int

@dataclass
class Order:
    table_number: int
    items: List[OrderItem] = field(default_factory=list)
    is_active: bool = True
    total_bill: float = 0.0
    tip: float = 0.0
    entry_time: datetime = field(default_factory=datetime.now)
    exit_time: datetime = None

class BiscottiCafe:
    def __init__(self):
        self.menu: Dict[FoodItem, MenuItem] = {
            FoodItem.COFFEE: MenuItem(FoodItem.COFFEE, 20.00, 5),
            FoodItem.TEA: MenuItem(FoodItem.TEA, 10.00, 3),
            FoodItem.SANDWICH: MenuItem(FoodItem.SANDWICH, 55.00, 10),
            FoodItem.BURGER: MenuItem(FoodItem.BURGER, 85.00, 15),
            FoodItem.FRIES: MenuItem(FoodItem.FRIES, 40.00, 8),
            FoodItem.CAKE: MenuItem(FoodItem.CAKE, 150.00, 5)
        }
        self.tables: int = 6
        self.orders: Dict[int, Order] = {}
        self.order_history: pd.DataFrame = pd.DataFrame(columns=[
            "Order ID", "Table Number", "Customer Order", "Total Bill", "Tip", "Entry Time", "Exit Time"
        ])
        self.order_id: int = 1
        self.current_session_history: pd.DataFrame = pd.DataFrame(columns=[
            "Order ID", "Table Number", "Customer Order", "Total Bill", "Tip", "Entry Time", "Exit Time"
        ])
        self.load_order_history()
        self.recommendations = self.load_recommendations()

    def load_order_history(self):
        if os.path.exists('customer_data.csv'):
            self.order_history = pd.read_csv('customer_data.csv')
            if not self.order_history.empty:
                self.order_id = self.order_history['Order ID'].max() + 1

    def load_recommendations(self):
        if os.path.exists('customer_data.csv'):
            df = pd.read_csv('customer_data.csv')
            df['Customer Order'] = df['Customer Order'].fillna('').astype(str)
            all_items = [re.findall(r'(\w+)\s*x\s*(\d+)', order) for order in df['Customer Order']]
            item_counts = Counter(item for order_items in all_items for item, _ in order_items)
            return [item for item, _ in item_counts.most_common(3)]
        return []

    def display_menu(self):
        print("\nMenu:")
        print("-" * 75)

        max_name_length = max(len(item.name.capitalize()) for item in self.menu) + 5
        max_price_length = max(len(f"{details.price:.2f} Rs") for details in self.menu.values()) + 5

        for index, (item, details) in enumerate(self.menu.items(), 1):
            name = item.name.capitalize()
            price = f"{details.price:.2f} Rs"
            prep_time = f"(Prep time: {details.prep_time} min)"
            print(f"{index}. {name.ljust(max_name_length)} {price.ljust(max_price_length)} {prep_time}")

        print("-" * 75)

        if self.recommendations:
            print("\nRecommended dishes based on popular orders:")
            print("--------------------------------------------")
            for index, dish in enumerate(self.recommendations, 1):
                print(f"--> {dish.capitalize()}")
        print()  # Extra newline for spacing

    def calculate_wait_time(self, order_items):
        total_wait_time = 0
        for item in order_items:
            item_wait_time = self.menu[item.item].prep_time
            scaled_wait_time = math.ceil((item.quantity / 4) * item_wait_time)
            total_wait_time += scaled_wait_time
        return total_wait_time

    def place_order(self, table_number: int):
        if table_number not in range(1, self.tables + 1):
            print(f"\nInvalid table number. Please choose a table between 1 and {self.tables}.")
            return

        if table_number not in self.orders or not self.orders[table_number].is_active:
            self.orders[table_number] = Order(table_number)
        
        order = self.orders[table_number]

        self.display_menu()
        while True:
            item_input = input("Enter item number or name (or 'done' or 'x' to finish): ")
            if item_input.lower() in ['done', 'x']:
                break

            try:
                if item_input.isdigit():
                    food_item = list(FoodItem)[int(item_input) - 1]
                else:
                    food_item = FoodItem[item_input.upper()]
            except (IndexError, KeyError):
                print("Invalid item. Please try again.")
                continue

            while True:
                try:
                    quantity = int(input("Enter quantity: "))
                    if quantity <= 0:
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid quantity. Please enter a positive integer.")

            order.items.append(OrderItem(food_item, quantity))

        if order.items:
            wait_time = self.calculate_wait_time(order.items)
            print(f"\nOrder placed for table {table_number}")
            print(f"Approximate waiting time: {wait_time} minutes")
        else:
            print("\nNo items ordered. Order cancelled.")
            self.orders.pop(table_number, None)

    def add_to_order(self, table_number: int):
        if table_number not in self.orders or not self.orders[table_number].is_active:
            print(f"\nNo active order for table {table_number}. Please place a new order.")
            return

        self.place_order(table_number)

    def close_order(self, table_number: int):
        if table_number not in self.orders or not self.orders[table_number].is_active:
            print(f"\nNo active order for table {table_number}.")
            return

        self.generate_bill(table_number)

    def generate_bill(self, table_number: int):
        order = self.orders[table_number]
        total = sum(self.menu[item.item].price * item.quantity for item in order.items)

        print(f"\nBill for Table {table_number}:")
        print("-" * 30)
        order_details = []
        for item in order.items:
            price = self.menu[item.item].price
            subtotal = price * item.quantity
            print(f"{item.item.name.capitalize()} x{item.quantity}: {subtotal:.2f} Rs")
            order_details.append(f"{item.item.name.capitalize()} x{item.quantity}")
        print("-" * 30)
        print(f"Total: {total:.2f} Rs")

        while True:
            choice = input("\nDid the customer tip? (y/n): ").lower()
            if choice == 'y':
                while True:
                    try:
                        tip = float(input("Enter tip amount: "))
                        if tip < 0:
                            raise ValueError
                        break
                    except ValueError:
                        print("Invalid tip amount. Please enter a non-negative number.")
                break
            elif choice == 'n':
                tip = 0.0
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

        order.exit_time = datetime.now()
        print(f"\nPayment received for table {table_number}. Order closed.")

        if order_details:
            new_order = pd.DataFrame({
                "Order ID": [self.order_id],
                "Table Number": [table_number],
                "Customer Order": [", ".join(order_details)],
                "Total Bill": [total],
                "Tip": [tip],
                "Entry Time": [order.entry_time.strftime("%Y-%m-%d %H:%M:%S")],
                "Exit Time": [order.exit_time.strftime("%Y-%m-%d %H:%M:%S")]
            })
            self.current_session_history = pd.concat([self.current_session_history, new_order], ignore_index=True)
            self.order_id += 1

        order.total_bill = total
        order.tip = tip
        order.is_active = False

    def display_order_history(self):
        print("\nOrder History for the Current Session:")
        print("---------------------------------------")
        if not self.current_session_history.empty:
            print(self.current_session_history.to_string(index=False))
        else:
            print("No orders in this session.")
        print()  # Extra newline for spacing

    def get_open_tables_with_orders(self):
        return [table for table, order in self.orders.items() if order.is_active]

    def close_all_tables(self):
        for table, order in self.orders.items():
            if order.is_active:
                self.generate_bill(table)

    def save_order_history(self):
        self.order_history = pd.concat([self.order_history, self.current_session_history], ignore_index=True)
        self.order_history.to_csv('customer_data.csv', index=False)
        self.recommendations = self.load_recommendations()  # Update recommendations after saving

    def run(self):
        while True:
            print("\nBiscotti Cafe Order System")
            print("==========================")
            print("1. Place Order")
            print("2. Add to Existing Order")
            print("3. Close Order and Generate Bill")
            print("4. Exit")
            print()  # Extra newline for spacing

            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                while True:
                    try:
                        open_tables = self.get_open_tables_with_orders()
                        closed_tables = [table for table in range(1, self.tables + 1) if table not in open_tables]
                        if closed_tables:
                            print("\nAvailable tables:", ", ".join(map(str, closed_tables)))
                        while True:
                            table = int(input("\nEnter table number: "))
                            if table in open_tables:
                                print(f"\nTable {table} already has an active order. Please choose another table.")
                            else:
                                break
                        break
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                self.place_order(table)
            elif choice == '2':
                open_tables = self.get_open_tables_with_orders()
                if open_tables:
                    print("\nOpen tables with active orders:", ", ".join(map(str, open_tables)))
                    while True:
                        try:
                            table = int(input("\nEnter table number: "))
                            break
                        except ValueError:
                            print("Invalid input. Please choose from the open tables.")
                    self.add_to_order(table)
                else:
                    print("\nNo open tables with active orders.")
            elif choice == '3':
                open_tables = self.get_open_tables_with_orders()
                if open_tables:
                    print("\nOpen tables with active orders:", ", ".join(map(str, open_tables)))
                    while True:
                        try:
                            table = int(input("\nEnter table number to close: "))
                            if table in open_tables:
                                break
                            else:
                                print("\nInvalid table number. Please choose from the open tables.")
                        except ValueError:
                            print("\nInvalid input. Please choose from the open tables.")
                    self.close_order(table)
                else:
                    print("\nNo open tables with active orders.")
            elif choice == '4':
                print("\nClosing all open tables...")
                self.close_all_tables()
                self.save_order_history()
                print("\nThank you for using Biscotti Cafe Order System. Goodbye!")
                self.display_order_history()
                break
            else:
                print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    cafe = BiscottiCafe()
    cafe.run()
