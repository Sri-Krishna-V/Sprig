'''
Membership
Purpose: Manages the membership features for customers.
Attributes:
customer_id: ID of the member.
discount_rate: Discount applicable for orders.
Methods:
apply_discount(): Applies a membership discount to an order.
check_membership_status(): Verifies if a customer is a member.
Abstraction: Encapsulates the details of discount logic.

'''

import sqlite3

DATABASE = 'sprig.db'


class Membership:
    def __init__(self, customer_id, discount_rate):
        self.customer_id = customer_id
        self.discount_rate = discount_rate

    def apply_discount(self, order_total):
        """
        Applies a membership discount to an order.
        """
        return order_total * (1 - self.discount_rate)

    def check_membership_status(self):
        """
        Verifies if a customer is a member.
        """
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT membership_status FROM Customers WHERE id=?
            ''', (self.customer_id,))
            status = cursor.fetchone()[0]
            conn.close()
            return status
        except sqlite3.Error as e:
            print(f"Database error during membership status check: {e}")
            return None
