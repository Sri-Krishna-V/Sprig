'''
Cart and CartItem
Purpose: Manages the items that a customer intends to purchase, acting as a temporary storage before an order is placed.

Attributes:

cart_id: Unique identifier for each cart.
customer_id: References the customer who owns this cart.
items: List of CartItem objects, representing individual items in the cart.
total_price: The cumulative price of all items in the cart.
Methods:

add_item(menu_item_id, quantity): Adds an item to the cart. Checks if the item is already in the cart, and if so, updates the quantity.
remove_item(cart_item_id): Removes an item from the cart by its ID.
update_quantity(cart_item_id, new_quantity): Adjusts the quantity of a specific item in the cart.
calculate_total(): Computes the total price for all items in the cart, considering membership discounts if applicable.
view_cart(): Displays the current items in the cart along with their quantities and the total price.
clear_cart(): Empties all items from the cart.
Encapsulation: The methods ensure that only the cart owner can modify its contents, and the calculations are handled internally for security.

'''

import sqlite3


DATABASE = 'sprig.db'


class Cart:
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.items = []
        self.total_price = 0

    def add_to_cart(self, menu_item_id, quantity):
        """
        Adds an item to the cart. Checks if the item is already in the cart, and if so, updates the quantity.
        """
        for item in self.items:
            if item.menu_item_id == menu_item_id:
                item.quantity += quantity
                return
        self.items.append(
            CartItem(None, self.customer_id, menu_item_id, quantity))

    def remove_from_cart(self, cart_item_id):
        """
        Removes an item from the cart by its ID.
        """
        for item in self.items:
            if item.cart_item_id == cart_item_id:
                self.items.remove(item)
                return

    def update_quantity(self, cart_item_id, new_quantity):
        """
        Adjusts the quantity of a specific item in the cart.
        """
        for item in self.items:
            if item.cart_item_id == cart_item_id:
                item.quantity = new_quantity
                return

    def calculate_total(self, membership_status):
        """
        Computes the total price for all items in the cart, considering membership discounts if applicable.
        """
        total = 0
        for item in self.items:
            total += item.calculate_subtotal()
        if membership_status == 'Gold':
            total *= 0.9
        elif membership_status == 'Silver':
            total *= 0.95
        self.total_price = total

    def view_cart(self):
        """
        Displays the current items in the cart along with their quantities and the total price.
        """
        for item in self.items:
            print(f"{item.menu_item_id}: {item.quantity}")
        print(f"Total Price: {self.total_price}")

    def clear_cart(self):
        """
        Empties all items from the cart.
        """
        self.items = []
        self.total_price = 0


class CartItem:
    def __init__(self, cart_item_id, customer_id, menu_item_id, quantity):
        self.cart_item_id = cart_item_id
        self.customer_id = customer_id
        self.menu_item_id = menu_item_id
        self.quantity = quantity

    def calculate_subtotal(self):
        """
        Calculates the total price for this item based on its quantity.
        """
        # Fetch the price of the menu item from the database
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT price FROM MenuItems WHERE id=?
            ''', (self.menu_item_id,))
            price = cursor.fetchone()[0]
            conn.close()
            return price * self.quantity
        except sqlite3.Error as e:
            print(f"Database error during subtotal calculation: {e}")
            return 0

'''
Cart and CartItem
Purpose: Manages the items that a customer intends to purchase, acting as a temporary storage before an order is placed.

Attributes:

cart_id: Unique identifier for each cart.
customer_id: References the customer who owns this cart.
items: List of CartItem objects, representing individual items in the cart.
total_price: The cumulative price of all items in the cart.
Methods:

add_item(menu_item_id, quantity): Adds an item to the cart. Checks if the item is already in the cart, and if so, updates the quantity.
remove_item(cart_item_id): Removes an item from the cart by its ID.
update_quantity(cart_item_id, new_quantity): Adjusts the quantity of a specific item in the cart.
calculate_total(): Computes the total price for all items in the cart, considering membership discounts if applicable.
view_cart(): Displays the current items in the cart along with their quantities and the total price.
clear_cart(): Empties all items from the cart.
Encapsulation: The methods ensure that only the cart owner can modify its contents, and the calculations are handled internally for security.

'''

import sqlite3


DATABASE = 'sprig.db'


class Cart:
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.items = []
        self.total_price = 0

    def add_to_cart(self, menu_item_id, quantity):
        """
        Adds an item to the cart. Checks if the item is already in the cart, and if so, updates the quantity.
        """
        for item in self.items:
            if item.menu_item_id == menu_item_id:
                item.quantity += quantity
                return
        self.items.append(
            CartItem(None, self.customer_id, menu_item_id, quantity))

    def remove_from_cart(self, cart_item_id):
        """
        Removes an item from the cart by its ID.
        """
        for item in self.items:
            if item.cart_item_id == cart_item_id:
                self.items.remove(item)
                return

    def update_quantity(self, cart_item_id, new_quantity):
        """
        Adjusts the quantity of a specific item in the cart.
        """
        for item in self.items:
            if item.cart_item_id == cart_item_id:
                item.quantity = new_quantity
                return

    def calculate_total(self, membership_status):
        """
        Computes the total price for all items in the cart, considering membership discounts if applicable.
        """
        total = 0
        for item in self.items:
            total += item.calculate_subtotal()
        if membership_status == 'Gold':
            total *= 0.9
        elif membership_status == 'Silver':
            total *= 0.95
        self.total_price = total

    def view_cart(self):
        """
        Displays the current items in the cart along with their quantities and the total price.
        """
        for item in self.items:
            print(f"{item.menu_item_id}: {item.quantity}")
        print(f"Total Price: {self.total_price}")

    def clear_cart(self):
        """
        Empties all items from the cart.
        """
        self.items = []
        self.total_price = 0


class CartItem:
    def __init__(self, cart_item_id, customer_id, menu_item_id, quantity):
        self.cart_item_id = cart_item_id
        self.customer_id = customer_id
        self.menu_item_id = menu_item_id
        self.quantity = quantity

    def calculate_subtotal(self):
        """
        Calculates the total price for this item based on its quantity.
        """
        # Fetch the price of the menu item from the database
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT price FROM MenuItems WHERE id=?
            ''', (self.menu_item_id,))
            price = cursor.fetchone()[0]
            conn.close()
            return price * self.quantity
        except sqlite3.Error as e:
            print(f"Database error during subtotal calculation: {e}")
            return 0
