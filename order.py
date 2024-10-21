'''
Order and OrderItem
Purpose: Manages orders placed by customers, tracking their status and the items within each order.

Attributes:

order_id: Unique identifier for each order.
customer_id: References the customer who placed the order.
restaurant_id: References the restaurant fulfilling the order.
status: Current status of the order (e.g., Pending, Preparing, Out for Delivery, Delivered).
order_date: Date and time when the order was placed.
total_amount: Final amount after applying discounts and membership benefits.
items: List of OrderItem objects, representing the items within the order.
Methods:

place_order(cart): Creates a new order using items from a given cart, calculates the total, and saves the order in the database.
update_order_status(new_status): Updates the status of an order (e.g., from "Pending" to "Preparing").
get_order_details(): Retrieves the details of a specific order, including items, status, and delivery information.
cancel_order(): Cancels an order if it’s in an allowable state, such as "Pending."
track_order(): Provides real-time status updates on the order’s progress.
Encapsulation: Methods like place_order() ensure that orders are created through a controlled process, protecting the order data's integrity.

'''

import sqlite3

DATABASE = 'sprig.db'


class Order:
    def __init__(self, order_id, customer_id, restaurant_id, status):
        self.order_id = order_id
        self.customer_id = customer_id
        self.restaurant_id = restaurant_id
        self.status = status

    def place_order(self, cart_items):
        """
        Creates a new order using items from a given cart, calculates the total, and saves the order in the database.
        """
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Orders (customer_id, restaurant_id, order_status)
                VALUES (?, ?, ?)
            ''', (self.customer_id, self.restaurant_id, 'Pending'))
            order_id = cursor.lastrowid
            for menu_item_id, quantity in cart_items:
                cursor.execute('''
                    INSERT INTO OrderItems (order_id, menu_item_id, quantity)
                    VALUES (?, ?, ?)
                ''', (order_id, menu_item_id, quantity))
            conn.commit()
            conn.close()
            return order_id
        except sqlite3.Error as e:
            print(f"Database error during order placement: {e}")
            return None

    def update_order_status(self, new_status):
        """
        Updates the status of an order (e.g., from "Pending" to "Preparing").
        """
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE Orders SET order_status=? WHERE id=?
            ''', (new_status, self.order_id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error during order status update: {e}")
            return False

    def get_order_details(self):
        """
        Retrieves the details of a specific order, including items, status, and delivery information.
        """
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT OrderItems.menu_item_id, OrderItems.quantity, MenuItems.item_name
                FROM OrderItems
                JOIN MenuItems ON OrderItems.menu_item_id = MenuItems.id
                WHERE OrderItems.order_id=?
            ''', (self.order_id,))
            items = cursor.fetchall()
            cursor.execute(
                'SELECT order_status FROM Orders WHERE id=?', (self.order_id,))
            status = cursor.fetchone()[0]
            conn.close()
            return items, status

        except sqlite3.Error as e:
            print(f"Database error during order details retrieval: {e}")
            return None

    def cancel_order(self):
        """
        Cancels an order if it's in an allowable state, such as "Pending."
        """
        if self.status == 'Pending':
            return self.update_order_status('Cancelled')
        else:
            return False

    def track_order(self):
        """
        Provides real-time status updates on the order's progress.
        """
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute(
                'SELECT order_status FROM Orders WHERE id=?', (self.order_id,))
            status = cursor.fetchone()[0]
            conn.close()
            return status
        except sqlite3.Error as e:
            print(f"Database error during order tracking: {e}")
            return None


class OrderItem:
    def __init__(self, order_item_id, order_id, menu_item_id, quantity):
        self.order_item_id = order_item_id
        self.order_id = order_id
        self.menu_item_id = menu_item_id
        self.quantity = quantity

    def update_quantity(self, new_quantity):
        """
        Changes the quantity of a specific item within an order.
        """
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE OrderItems SET quantity=? WHERE id=?
            ''', (new_quantity, self.order_item_id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error during order item update: {e}")
            return False

    def remove_item(self):
        """
        Deletes an item from the order.
        """
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM OrderItems WHERE id=?
            ''', (self.order_item_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error during order item removal: {e}")
            return False
