'''
Refer main.py file for the complete and accurate code.

'''

import re


def validate_id(id):
    """
    Validates an ID to ensure it is a positive integer.
    """
    if isinstance(id, int) and id > 0:
        return True, ""
    return False, "ID must be a positive integer."


def validate_name(name):
    """
    Validates a name to ensure it only contains alphabetic characters.
    """
    if name.isalpha():
        return True, ""
    return False, "Name must contain only alphabetic characters."


def validate_username(username):
    """
    Validates a username to ensure it meets criteria:
    - Must be between 3 and 30 characters.
    - Only allows alphanumeric characters and underscores.
    """
    if re.match(r'^\w{3,30}$', username):
        return True, ""
    return False, "Username must be between 3 and 30 characters and can only contain letters, numbers, and underscores."


def validate_password(password):
    """
    Validates a password to ensure it meets criteria:
    - Minimum 8 characters.
    - Must contain at least one uppercase letter, one lowercase letter, one digit, and one special character.
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character."
    return True, ""


def validate_email(email):
    """
    Validates an email address format.
    """
    if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        return True, ""
    return False, "Invalid email format."


def validate_phone_number(phone_number):
    """
    Validates phone number to ensure it follows a common 10-digit pattern.
    """
    if re.match(r'^\d{10}$', phone_number):
        return True, ""
    return False, "Phone number must be 10 digits long."


def validate_user_type(user_type):
    """
    Validates user type to ensure it is one of the allowed types.
    """
    allowed_types = {'Customer', 'RestaurantPartner', 'DeliveryPartner'}
    if user_type in allowed_types:
        return True, ""
    return False, f"User type must be one of {allowed_types}."


def validate_membership_type(membership_type):
    """
    Validates membership type.
    """
    allowed_types = {'Basic', 'Premium', 'Gold'}
    if membership_type in allowed_types:
        return True, ""
    return False, f"Membership type must be one of {allowed_types}."


def validate_discount_rate(discount_rate):
    """
    Validates that the discount rate is between 0 and 100.
    """
    if 0 <= discount_rate <= 100:
        return True, ""
    return False, "Discount rate must be between 0 and 100."


def validate_restaurant_name(restaurant_name):
    """
    Validates restaurant name to ensure it is not empty and has a reasonable length.
    """
    if 1 <= len(restaurant_name) <= 100:
        return True, ""
    return False, "Restaurant name must be between 1 and 100 characters."


def validate_price(price):
    """
    Validates that the price is a positive number.
    """
    if price >= 0:
        return True, ""
    return False, "Price must be a positive number."


def validate_quantity(quantity):
    """
    Validates that the quantity is a positive integer.
    """
    if isinstance(quantity, int) and quantity > 0:
        return True, ""
    return False, "Quantity must be a positive integer."


def validate_vehicle_number(vehicle_number):
    """
    Validates vehicle number format. Adjust the regex pattern based on local formats.
    """
    if re.match(r'^[A-Z0-9-]{5,10}$', vehicle_number):
        return True, ""
    return False, "Vehicle number must be alphanumeric and between 5 to 10 characters."


def validate_order_status(order_status):
    """
    Validates order status to ensure it is one of the allowed values.
    """
    allowed_statuses = {'Pending', 'Preparing',
                        'Out for Delivery', 'Delivered'}
    if order_status in allowed_statuses:
        return True, ""
    return False, f"Order status must be one of {allowed_statuses}."


def validate_payment_method(payment_method):
    """
    Validates payment method to ensure it is supported.
    """
    allowed_methods = {'Credit Card', 'Debit Card', 'UPI', 'Cash on Delivery'}
    if payment_method in allowed_methods:
        return True, ""
    return False, f"Payment method must be one of {allowed_methods}."


def validate_payment_status(payment_status):
    """
    Validates payment status to ensure it is one of the allowed values.
    """
    allowed_statuses = {'Pending', 'Completed', 'Refunded'}
    if payment_status in allowed_statuses:
        return True, ""
    return False, f"Payment status must be one of {allowed_statuses}."


def validate_date_format(date_text):
    """
    Validates date format to ensure it follows 'YYYY-MM-DD'.
    """
    try:
        from datetime import datetime
        datetime.strptime(date_text, '%Y-%m-%d')
        return True, ""
    except ValueError:
        return False, "Date must be in 'YYYY-MM-DD' format."


def validate_description(description):
    """
    Validates description to ensure it is not empty and has a reasonable length.
    """
    if 1 <= len(description) <= 500:
        return True, ""
    return False, "Description must be between 1 and 500 characters."


def validate_status(status):
    """
    Validates status to ensure it is not empty and has a reasonable length.
    """
    if 1 <= len(status) <= 50:
        return True, ""
    return False, "Status must be between 1 and 50 characters."


def validate_address(address):
    """
    Validates address to ensure it is not empty and has a reasonable length.
    """
    if 1 <= len(address) <= 200:
        return True, ""
    return False, "Address must be between 1 and 200 characters."
