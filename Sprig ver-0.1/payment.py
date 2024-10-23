'''
Payment (Inheriting from Order, Customer, Cart, and Membership classes):
Purpose: Handles payments for customer orders, ensuring transactions are secure and processed correctly.

Attributes:

payment_id: Unique identifier for each payment.
order_id: Associated order that the payment is tied to.
customer_id: References the customer making the payment.
amount: Total payment amount.
payment_method: Specifies the payment method used (e.g., credit card, debit card, UPI).
payment_status: Status of the transaction (e.g., "Pending", "Completed", "Failed", "Refunded").
transaction_date: The date and time when the transaction occurred.
Methods:

process_payment(payment_method, details): Initiates the payment process using the specified method and details. Verifies payment through integration with a payment gateway.
verify_payment(): Confirms if the payment has been processed successfully, updating the payment_status to "Completed" if verification is successful.
refund_payment(reason): Handles refunds in case of issues such as order cancellation. Changes payment_status to "Refunded" and logs the reason for the refund.
get_payment_status(): Retrieves the current status of the payment for tracking purposes.
calculate_final_amount(cart_total, discounts): Calculates the final payable amount, applying discounts or membership benefits (if applicable).
Encapsulation: Sensitive details related to transactions are managed internally, and only relevant methods are exposed to ensure secure payment processing.

'''

import sqlite3
from order import Order
from customer import Customer
from cart import Cart
from membership import Membership

DATABASE = 'sprig.db'


class Payment(Order, Customer, Cart, Membership):
    def __init__(self, payment_id, order_id, customer_id, amount, payment_method, payment_status, transaction_date):
        super().__init__(order_id, customer_id, None, None)
        self.payment_id = payment_id
        self.amount = amount
        self.payment_method = payment_method
        self.payment_status = payment_status
        self.transaction_date = transaction_date

    def payment_details(self):
        """
        Displays the payment details for reference.
        """
        print(f"Payment ID: {self.payment_id}")
        print(f"Order ID: {self.order_id}")
        print(f"Amount: {self.amount}")
        print(f"Payment Method: {self.payment_method}")
        print(f"Payment Status: {self.payment_status}")
        print(f"Transaction Date: {self.transaction_date}")

    def process_payment(self, payment_method):
        """
        Initiates the payment process using the specified method and details. Verifies payment through integration with a payment gateway.
        For simplicity, this method will just simulate a successful payment.
        """
        print(f"Processing payment with {payment_method}...")

        if payment_method in ["Credit Card", "Debit Card", "UPI"]:
            self.payment_status = "Completed"
            print("Payment successful.")
        else:
            self.payment_status = "Failed"
            print("Payment failed. Invalid payment method.")

    def verify_payment(self):
        """
        Confirms if the payment has been processed successfully, updating the payment_status to "Completed" if verification is successful.
        Here, we'll simulate verification as always successful for demonstration.
        """
        if self.payment_status == "Completed":
            print("Payment verified successfully.")
        else:
            print("Payment verification failed. Please retry.")

    def refund_payment(self, reason):
        """
        Handles refunds in case of issues such as order cancellation. Changes payment_status to "Refunded" and logs the reason for the refund.
        """
        if self.payment_status == "Completed":
            self.payment_status = "Refunded"
            print(f"Payment refunded successfully. Reason: {reason}")
        else:
            print("Refund not possible. Payment was not completed.")

    def get_payment_status(self):
        """
        Retrieves the current status of the payment for tracking purposes.
        """
        return self.payment_status

    def calculate_final_amount(self, cart_total, discounts):
        """
        Calculates the final payable amount, applying discounts or membership benefits (if applicable).
        For simplicity, it subtracts the discount from the total.
        """
        final_amount = cart_total - discounts
        print(f"Final amount after applying discounts: {final_amount}")
        return final_amount

'''
Payment (Inheriting from Order, Customer, Cart, and Membership classes):
Purpose: Handles payments for customer orders, ensuring transactions are secure and processed correctly.

Attributes:

payment_id: Unique identifier for each payment.
order_id: Associated order that the payment is tied to.
customer_id: References the customer making the payment.
amount: Total payment amount.
payment_method: Specifies the payment method used (e.g., credit card, debit card, UPI).
payment_status: Status of the transaction (e.g., "Pending", "Completed", "Failed", "Refunded").
transaction_date: The date and time when the transaction occurred.
Methods:

process_payment(payment_method, details): Initiates the payment process using the specified method and details. Verifies payment through integration with a payment gateway.
verify_payment(): Confirms if the payment has been processed successfully, updating the payment_status to "Completed" if verification is successful.
refund_payment(reason): Handles refunds in case of issues such as order cancellation. Changes payment_status to "Refunded" and logs the reason for the refund.
get_payment_status(): Retrieves the current status of the payment for tracking purposes.
calculate_final_amount(cart_total, discounts): Calculates the final payable amount, applying discounts or membership benefits (if applicable).
Encapsulation: Sensitive details related to transactions are managed internally, and only relevant methods are exposed to ensure secure payment processing.

'''

import sqlite3
from order import Order
from customer import Customer
from cart import Cart
from membership import Membership

DATABASE = 'sprig.db'


class Payment(Order, Customer, Cart, Membership):
    def __init__(self, payment_id, order_id, customer_id, amount, payment_method, payment_status, transaction_date):
        super().__init__(order_id, customer_id, None, None)
        self.payment_id = payment_id
        self.amount = amount
        self.payment_method = payment_method
        self.payment_status = payment_status
        self.transaction_date = transaction_date

    def payment_details(self):
        """
        Displays the payment details for reference.
        """
        print(f"Payment ID: {self.payment_id}")
        print(f"Order ID: {self.order_id}")
        print(f"Amount: {self.amount}")
        print(f"Payment Method: {self.payment_method}")
        print(f"Payment Status: {self.payment_status}")
        print(f"Transaction Date: {self.transaction_date}")

    def process_payment(self, payment_method):
        """
        Initiates the payment process using the specified method and details. Verifies payment through integration with a payment gateway.
        For simplicity, this method will just simulate a successful payment.
        """
        print(f"Processing payment with {payment_method}...")

        if payment_method in ["Credit Card", "Debit Card", "UPI"]:
            self.payment_status = "Completed"
            print("Payment successful.")
        else:
            self.payment_status = "Failed"
            print("Payment failed. Invalid payment method.")

    def verify_payment(self):
        """
        Confirms if the payment has been processed successfully, updating the payment_status to "Completed" if verification is successful.
        Here, we'll simulate verification as always successful for demonstration.
        """
        if self.payment_status == "Completed":
            print("Payment verified successfully.")
        else:
            print("Payment verification failed. Please retry.")

    def refund_payment(self, reason):
        """
        Handles refunds in case of issues such as order cancellation. Changes payment_status to "Refunded" and logs the reason for the refund.
        """
        if self.payment_status == "Completed":
            self.payment_status = "Refunded"
            print(f"Payment refunded successfully. Reason: {reason}")
        else:
            print("Refund not possible. Payment was not completed.")

    def get_payment_status(self):
        """
        Retrieves the current status of the payment for tracking purposes.
        """
        return self.payment_status

    def calculate_final_amount(self, cart_total, discounts):
        """
        Calculates the final payable amount, applying discounts or membership benefits (if applicable).
        For simplicity, it subtracts the discount from the total.
        """
        final_amount = cart_total - discounts
        print(f"Final amount after applying discounts: {final_amount}")
        return final_amount
