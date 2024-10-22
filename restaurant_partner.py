'''
RestaurantPartner (Inherits from User)
Purpose: Manages a restaurant's presence on the platform.
Attributes:
partner_id: Inherited from User.
restaurant_id: ID associated with the restaurant they manage.
Methods:
add_menu_item(): Allows partners to add new dishes to the menu.
remove_menu_item(): Removes a dish from the menu.
view_orders(): Retrieves current orders for their restaurant.
update_order_status(): Changes the status of orders to reflect their progress.
Polymorphism: update_order_status() behaves differently compared to delivery partners.

'''

import sqlite3
import hashlib
from user import User


DATABASE = 'sprig.db'


class RestaurantPartner(User):
    def __init__(self, username, password, partner_id, restaurant_id):
        super().__init__(username, password)
        self.partner_id = partner_id
        self.restaurant_id = restaurant_id

    @classmethod
    def signup(cls, username, password, restaurant_name, address, cuisine):
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Users (username, password, name, email, user_type)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, hashlib.sha256(password.encode()).hexdigest(), restaurant_name, f"{username}@sprig.com", 'RestaurantPartner'))
            user_id = cursor.lastrowid
            cursor.execute('''
                INSERT INTO Restaurants (restaurant_name, address, cuisine_type)
                VALUES (?, ?, ?)
            ''', (restaurant_name, address, cuisine))
            restaurant_id = cursor.lastrowid
            cursor.execute('''
                INSERT INTO RestaurantPartners (id, restaurant_id, address, cuisine_type)
                VALUES (?, ?, ?, ?)
            ''', (user_id, restaurant_id, address, cuisine))
            conn.commit()
            restaurant_partner = cls(user_id, username, password, restaurant_name, address, cuisine)
            conn.close()
            return restaurant_partner
        except sqlite3.Error as e:
            print(f"Database error during restaurant partner signup: {e}")
            return None

    def add_menu_item(self, item_name, price, description):
        """
        Allows partners to add new dishes to the menu.
        """
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO MenuItems (restaurant_id, item_name, price, item_description)
                VALUES (?, ?, ?, ?)
            ''', (self.restaurant_id, item_name, price, description))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error during menu item addition: {e}")
            return False

    def remove_menu_item(self, menu_item_id):
        """
        Removes a dish from the menu.
        """
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM MenuItems WHERE id=?
            ''', (menu_item_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error during menu item removal: {e}")
            return False

    def view_orders(self):
        """
        Retrieves current orders for their restaurant.
        """
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT Orders.id, Orders.customer_id, Orders.order_status
                FROM Orders
                WHERE Orders.restaurant_id=?
            ''', (self.restaurant_id,))
            orders = cursor.fetchall()
            conn.close()
            return orders
        except sqlite3.Error as e:
            print(f"Database error during order retrieval: {e}")
            return None

    def update_order_status(self, order_id, status):
        """
        Changes the status of orders to reflect their progress.
        """
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE Orders SET order_status=? WHERE id=?
            ''', (status, order_id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error during order status update: {e}")
            return False
