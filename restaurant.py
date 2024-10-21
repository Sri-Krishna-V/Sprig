'''
Restaurant
Purpose: Represents restaurant information and menu management.
Attributes:
restaurant_id: Unique identifier.
name: Restaurant's name.
address: Location of the restaurant.
Methods:
get_menu(): Fetches menu items for display.
get_restaurant_list(): Returns a list of available restaurants.
Abstraction: Shields the complex database interactions from the partner class.

'''

import sqlite3

DATABASE = 'sprig.db'


class Restaurant:
    def __init__(self, restaurant_id, name, address):
        self.restaurant_id = restaurant_id
        self.name = name
        self.address = address

    def get_menu(self):
        """
        Fetches menu items for display.
        """
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM MenuItems WHERE restaurant_id=?', (self.restaurant_id,))
            menu_items = cursor.fetchall()
            conn.close()
            return menu_items
        except sqlite3.Error as e:
            print(f"Database error during menu retrieval: {e}")
            return []

    @staticmethod
    def get_restaurant_list():
        """
        Returns a list of available restaurants.
        """
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Restaurants')
            restaurants = cursor.fetchall()
            conn.close()
            return restaurants
        except sqlite3.Error as e:
            print(f"Database error during restaurant list retrieval: {e}")
            return []
