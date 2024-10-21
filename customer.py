'''
Customer (Inherits from User)
Purpose: Represents the customer's actions and interactions.
Attributes:
customer_id: Inherited from User.
membership_status: Tracks if a customer is a member.
Methods:
view_restaurants(): Displays available restaurants.
view_menu(): Shows menu items from a selected restaurant.
add_to_cart(): Adds menu items to a cart.
place_order(): Confirms an order based on cart contents.
view_order_history(): Displays past orders.
Abstraction: Hides the complexities of interacting with restaurant data.

'''

import sqlite3
from user import *
from restaurant import *
from cart import *
from order import *

DATABASE = 'sprig.db'


class Customer(User):
    def __init__(self, username, password, customer_id, membership_status):
        super().__init__(username, password)
        self.customer_id = customer_id
        self.membership_status = membership_status

    def view_restaurants(self):
        """
        Displays available restaurants.
        """
        return Restaurant.get_restaurant_list()

    def view_menu(self, restaurant_id):
        """
        Shows menu items from a selected restaurant.
        """
        restaurant = Restaurant(restaurant_id, '', '')
        return restaurant.get_menu()

    def add_to_cart(self, cart_items):
        """
        Adds menu items to a cart.
        - cart_items: list of (menu_item_id, quantity) tuples.
        """
        cart = Cart(self.customer_id)
        for menu_item_id, quantity in cart_items:
            cart.add_to_cart(menu_item_id, quantity)

    def place_order(self):
        """
        Confirms an order based on cart contents.
        """
        cart = Cart(self.customer_id)
        cart_items = cart.get_cart_items()
        order = Order(None, self.customer_id, None, None)
        return order.place_order(cart_items)

    def view_order_history(self):
        """
        Displays past orders.
        """
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT Orders.id, Orders.order_status, Orders.order_date, Restaurants.name
                FROM Orders
                JOIN Restaurants ON Orders.restaurant_id=Restaurants.id
                WHERE Orders.customer_id=?
            ''', (self.customer_id,))
            orders = cursor.fetchall()
            conn.close()
            return orders
        except sqlite3.Error as e:
            print(f"Database error during order history retrieval: {e}")
            return []
