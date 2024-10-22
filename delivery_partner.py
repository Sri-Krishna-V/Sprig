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
import hashlib
from user import User

DATABASE = 'sprig.db'


class DeliveryPartner(User):
    @classmethod
    def signup(cls, username, password, name, vehicle_type, license_number):
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Users (username, password, name, email, user_type)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, hashlib.sha256(password.encode()).hexdigest(), name, f"{username}@sprig.com", 'DeliveryPartner'))
            user_id = cursor.lastrowid
            cursor.execute('''
                INSERT INTO DeliveryPartners (id, vehicle_type, license_number)
                VALUES (?, ?, ?)
            ''', (user_id, vehicle_type, license_number))
            conn.commit()
            delivery_partner = cls(
                user_id, username, password, name, vehicle_type, license_number)
            conn.close()
            return delivery_partner
        except sqlite3.Error as e:
            print(f"Database error during delivery partner signup: {e}")
            return None

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
