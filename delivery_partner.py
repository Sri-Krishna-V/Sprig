'''
DeliveryPartner (Inherits from User)
Purpose: Manages order deliveries.
Attributes:
partner_id: Inherited from User.
Methods:
view_assigned_orders(): Shows orders assigned for delivery.
update_order_status(): Updates delivery status (e.g., In Transit, Delivered).
view_earnings(): Shows total earnings from completed deliveries.
Encapsulation: Hides the complexities of order management from other entities.

'''

import sqlite3
from user import User

DATABASE = 'sprig.db'


class DeliveryPartner(User):
    def __init__(self, username, password, partner_id):
        super().__init__(username, password)
        self.partner_id = partner_id

    def view_assigned_orders(self):
        """
        Shows orders assigned for delivery.
        """
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT Orders.id, Orders.order_status, Orders.order_date, Restaurants.restaurant_name
                FROM Orders
                JOIN Restaurants ON Orders.restaurant_id = Restaurants.id
                WHERE Orders.delivery_partner_id=?
            ''', (self.partner_id,))
            orders = cursor.fetchall()
            conn.close()
            return orders
        except sqlite3.Error as e:
            print(f"Database error during order retrieval: {e}")
            return None

    def update_order_status(self, order_id, status):
        """
        Updates delivery status (e.g., In Transit, Delivered).
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

    def view_earnings(self):
        """
        Shows total earnings from completed deliveries.
        """
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT SUM(amount) FROM Payments WHERE delivery_partner_id=?
            ''', (self.partner_id,))
            earnings = cursor.fetchone()[0]
            conn.close()
            return earnings
        except sqlite3.Error as e:
            print(f"Database error during earnings retrieval: {e}")
            return None
