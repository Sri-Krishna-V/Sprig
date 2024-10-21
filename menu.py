'''
Menu and MenuItem
Purpose: Represents and manages the menu for restaurants, allowing them to control what customers can order.

Attributes:

menu_id: Unique identifier for each menu.
restaurant_id: References the restaurant to which the menu belongs.
items: List of MenuItem objects associated with this menu.
Methods:

add_menu_item(item_name, price, description, availability): Adds a new item to the menu with specified details.
remove_menu_item(menu_item_id): Removes an item from the menu.
update_menu_item(menu_item_id, new_details): Updates the name, price, description, or availability of an item.
get_menu(): Retrieves the list of all menu items available at the restaurant.
get_item_details(menu_item_id): Fetches detailed information about a specific menu item.
update_availability(menu_item_id, is_available): Updates the availability of a specific item based on stock or seasonal availability.
Encapsulation: Restaurants can manage their menu items securely, while only exposing necessary methods to the customer interface.

'''

import sqlite3

DATABASE = 'sprig.db'


class Menu:
    def __init__(self, menu_id, restaurant_id):
        self.menu_id = menu_id
        self.restaurant_id = restaurant_id
        self.items = []

    def add_menu_item(self, item_name, price, description, availability):
        """
        Adds a new item to the menu with specified details.
        """
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO MenuItems (restaurant_id, item_name, price, description, availability)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.restaurant_id, item_name, price, description, availability))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error during menu item addition: {e}")
            return False

    def remove_menu_item(self, menu_item_id):
        """
        Removes an item from the menu.
        """
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM MenuItems WHERE menu_item_id=?
            ''', (menu_item_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error during menu item removal: {e}")
            return False

    def update_menu_item(self, menu_item_id, new_details):
        """
        Updates the name, price, description, or availability of an item.
        """
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE MenuItems
                SET item_name=?, price=?, description=?, availability=?
                WHERE menu_item_id=?
            ''', (*new_details, menu_item_id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error during menu item update: {e}")
            return False

    def get_menu(self):
        """
        Retrieves the list of all menu items available at the restaurant.
        """
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM MenuItems WHERE restaurant_id=?
            ''', (self.restaurant_id,))
            menu_items = cursor.fetchall()
            conn.close()
            return menu_items
        except sqlite3.Error as e:
            print(f"Database error during menu retrieval: {e}")
            return []

    def get_item_details(self, menu_item_id):
        """
        Fetches detailed information about a specific menu item.
        """
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM MenuItems WHERE id=?
            ''', (menu_item_id,))
            item_details = cursor.fetchone()
            conn.close()
            return item_details
        except sqlite3.Error as e:
            print(f"Database error during item details retrieval: {e}")
            return None

    def update_availability(self, menu_item_id, is_available):
        """
        Updates the availability of a specific item based on stock or seasonal availability.
        """
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE MenuItems SET availability=? WHERE id=?
            ''', (is_available, menu_item_id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error during availability update: {e}")
            return False


class MenuItem:
    def __init__(self, menu_item_id, restaurant_id, item_name, price, description, availability):
        self.menu_item_id = menu_item_id
        self.restaurant_id = restaurant_id
        self.item_name = item_name
        self.price = price
        self.description = description
        self.availability = availability

    def __str__(self):
        return f"{self.item_name} - ${self.price} ({'Available' if self.availability else 'Not Available'})"
