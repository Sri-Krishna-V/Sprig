'''
Access all the functions from the other files and build a robust main function. 
Remember to use the functions from the other files to build the main function.
Follow best practices and use the functions from the other files to build the main function.
Refer database.py for the database schema.
Refer validations.py for the validation functions and error messages.

'''

from menu import Menu
from restaurant import Restaurant
from customer import Customer
from order import Order
from cart import Cart, CartItem
from user import User
from restaurant_partner import RestaurantPartner
from delivery_partner import DeliveryPartner
from membership import Membership
from payment import Payment
from utils.validations import (
    validate_username, validate_password, validate_id, validate_quantity,
    validate_name, validate_price, validate_description, validate_status,
    validate_email, validate_phone_number
)
from utils.database import initialize_database, get_db_connection

DATABASE = 'sprig.db'


def main():
    try:
        initialize_database()  # Move initialization here
        print("Welcome to Sprig!")
        while True:
            print("1. Customer")
            print("2. Restaurant Partner")
            print("3. Delivery Partner")
            print("4. Exit")
            choice = input("Enter your role: ")

            if choice == "1":
                customer_flow()
            elif choice == "2":
                restaurant_partner_flow()
            elif choice == "3":
                delivery_partner_flow()
            elif choice == "4":
                print("Thank you for using Sprig!")
                break
            else:
                print("Invalid choice. Please try again.")
    except Exception as e:
        print(f"Error starting application: {str(e)}")
        return


def customer_flow():
    print("1. Sign In")
    print("2. Sign Up")
    auth_choice = input("Enter your choice: ")

    if auth_choice == "1":
        customer = customer_login()
        if customer:
            customer_menu(customer)
    elif auth_choice == "2":
        if customer_signup():
            print("Sign up successful! Please login.")
            customer = customer_login()
            if customer:
                customer_menu(customer)
    else:
        print("Invalid choice. Please try again.")


def customer_login():
    print("Customer Login")
    username = input("Enter username: ")
    password = input("Enter password: ")
    if validate_username(username) and validate_password(password):
        customer = Customer.login(username, password)
        if customer:
            print("Login successful!")
            return customer
        else:
            print("Invalid credentials. Please try again.")
    else:
        print("Invalid username or password format. Please try again.")
    return None


def customer_menu(customer):
    print("1. View Restaurants")
    print("2. View Menu")
    print("3. Add to Cart")
    print("4. Place Order")
    print("5. View Order History")
    print("6. Logout")
    choice = input("Enter your choice: ")

    if choice == "1":
        view_restaurants(customer)
    elif choice == "2":
        view_menu(customer)
    elif choice == "3":
        add_to_cart(customer)
    elif choice == "4":
        place_order(customer)
    elif choice == "5":
        view_order_history(customer)
    elif choice == "6":
        print("Logging out...")
    else:
        print("Invalid choice. Please try again.")
        customer_menu(customer)


def view_restaurants(customer):
    print("Available Restaurants:")
    restaurants = Restaurant.get_restaurant_list()
    for restaurant in restaurants:
        print(f"{restaurant[0]}. {restaurant[1]}")
    customer_menu(customer)


def view_menu(customer):
    restaurant_id = input("Enter restaurant ID: ")
    if validate_id(restaurant_id):
        restaurant = Restaurant(restaurant_id, '', '')
        menu = restaurant.get_menu()
        if menu:
            print("Menu:")
            for item in menu:
                print(f"{item[0]}. {item[1]} - {item[2]}")
        else:
            print("Invalid restaurant ID. Please try again.")
    else:
        print("Invalid restaurant ID. Please try again.")
    customer_menu(customer)


def add_to_cart(customer):
    cart = Cart(customer.customer_id)
    menu_item_id = input("Enter menu item ID: ")
    quantity = input("Enter quantity: ")
    if validate_id(menu_item_id) and validate_quantity(quantity):
        cart.add_to_cart(menu_item_id, quantity)
        print("Item added to cart.")
    else:
        print("Invalid input. Please try again.")
    customer_menu(customer)


def place_order(customer):
    cart = Cart(customer.customer_id)
    cart_items = cart.get_cart_items()
    if cart_items:
        order = Order(None, customer.customer_id, None, None)
        order_id = order.place_order(cart_items)
        if order_id:
            print(f"Order placed successfully! Order ID: {order_id}")
        else:
            print("Failed to place order. Please try again.")
    else:
        print("Cart is empty. Please add items to cart.")
    customer_menu(customer)


def view_order_history(customer):
    orders = Order.get_order_history(customer.customer_id)
    if orders:
        print("Order History:")
        for order in orders:
            print(f"Order ID: {order[0]}, Status: {order[1]}")
    else:
        print("No orders found.")
    customer_menu(customer)


def restaurant_partner_login():
    print("Restaurant Partner Login")
    username = input("Enter username: ")
    password = input("Enter password: ")
    if validate_username(username) and validate_password(password):
        restaurant_partner = RestaurantPartner.login(username, password)
        if restaurant_partner:
            print("Login successful!")
            return restaurant_partner
        else:
            print("Invalid credentials. Please try again.")
    else:
        print("Invalid username or password. Please try again.")
    return None


def restaurant_partner_menu(restaurant_partner):
    print("1. Add Menu Item")
    print("2. Remove Menu Item")
    print("3. View Orders")
    print("4. Logout")
    choice = input("Enter your choice: ")

    if choice == "1":
        add_menu_item(restaurant_partner)
    elif choice == "2":
        remove_menu_item(restaurant_partner)
    elif choice == "3":
        view_orders(restaurant_partner)
    elif choice == "4":
        print("Logging out...")
    else:
        print("Invalid choice. Please try again.")
        restaurant_partner_menu(restaurant_partner)


def add_menu_item(restaurant_partner):
    item_name = input("Enter item name: ")
    price = input("Enter price: ")
    description = input("Enter description: ")
    if validate_name(item_name) and validate_price(price) and validate_description(description):
        if restaurant_partner.add_menu_item(item_name, price, description):
            print("Menu item added successfully!")
        else:
            print("Failed to add menu item. Please try again.")
    else:
        print("Invalid input. Please try again.")
    restaurant_partner_menu(restaurant_partner)


def remove_menu_item(restaurant_partner):
    menu_item_id = input("Enter menu item ID: ")
    if validate_id(menu_item_id):
        if restaurant_partner.remove_menu_item(menu_item_id):
            print("Menu item removed successfully!")
        else:
            print("Failed to remove menu item. Please try again.")
    else:
        print("Invalid menu item ID. Please try again.")
    restaurant_partner_menu(restaurant_partner)


def view_orders(restaurant_partner):
    orders = restaurant_partner.view_orders()
    if orders:
        print("Orders:")
        for order in orders:
            print(f"Order ID: {order[0]}, Customer ID: {
                  order[1]}, Status: {order[2]}")
    else:
        print("No orders found.")
    restaurant_partner_menu(restaurant_partner)


def delivery_partner_login():
    print("Delivery Partner Login")
    username = input("Enter username: ")
    password = input("Enter password: ")
    if validate_username(username) and validate_password(password):
        delivery_partner = DeliveryPartner.login(username, password)
        if delivery_partner:
            print("Login successful!")
            return delivery_partner
        else:
            print("Invalid credentials. Please try again.")
    else:
        print("Invalid username or password. Please try again.")
    return None


def delivery_partner_menu(delivery_partner):
    print("1. View Assigned Orders")
    print("2. Update Order Status")
    print("3. View Earnings")
    print("4. Logout")
    choice = input("Enter your choice: ")

    if choice == "1":
        view_assigned_orders(delivery_partner)
    elif choice == "2":
        update_order_status(delivery_partner)
    elif choice == "3":
        view_earnings(delivery_partner)
    elif choice == "4":
        print("Logging out...")
    else:
        print("Invalid choice. Please try again.")
        delivery_partner_menu(delivery_partner)


def view_assigned_orders(delivery_partner):
    orders = delivery_partner.view_assigned_orders()
    if orders:
        print("Assigned Orders:")
        for order in orders:
            print(f"Order ID: {order[0]}, Status: {order[1]}, Date: {
                  order[2]}, Restaurant: {order[3]}")
    else:
        print("No assigned orders found.")
    delivery_partner_menu(delivery_partner)


def update_order_status(delivery_partner):
    order_id = input("Enter order ID: ")
    status = input("Enter order status: ")
    if validate_id(order_id) and validate_status(status):
        if delivery_partner.update_order_status(order_id, status):
            print("Order status updated successfully!")
        else:
            print("Failed to update order status. Please try again.")
    else:
        print("Invalid input. Please try again.")
    delivery_partner_menu(delivery_partner)


def view_earnings(delivery_partner):
    earnings = delivery_partner.get_earnings()
    if earnings:
        print(f"Earnings: {earnings}")
    else:
        print("No earnings found.")
    delivery_partner_menu(delivery_partner)


def customer_signup():
    print("Customer Sign Up")
    username = input("Enter username: ")
    password = input("Enter password: ")
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    phone = input("Enter your phone number: ")

    if (validate_username(username) and validate_password(password) and
        validate_name(name) and validate_email(email) and validate_phone_number(phone)):
        customer = Customer.signup(username, password, name, email, phone)
        if customer:
            return True
        else:
            print("Failed to sign up. Please try again.")
    else:
        print("Invalid input. Please check your entries and try again.")
    return False


def restaurant_partner_signup():
    print("Restaurant Partner Sign Up")
    username = input("Enter username: ")
    password = input("Enter password: ")
    restaurant_name = input("Enter restaurant name: ")
    address = input("Enter restaurant address: ")
    cuisine = input("Enter cuisine type: ")

    if validate_username(username) and validate_password(password):
        restaurant_partner = RestaurantPartner.signup(
            username, password, restaurant_name, address, cuisine)
        if restaurant_partner:
            print("Sign up successful!")
            return True
        else:
            print("Failed to sign up. Please try again.")
    else:
        print("Invalid username or password. Please try again.")
    return False


def delivery_partner_signup():
    print("Delivery Partner Sign Up")
    username = input("Enter username: ")
    password = input("Enter password: ")
    name = input("Enter your name: ")
    vehicle_type = input("Enter your vehicle type: ")
    license_number = input("Enter your license number: ")

    if validate_username(username) and validate_password(password):
        delivery_partner = DeliveryPartner.signup(
            username, password, name, vehicle_type, license_number)
        if delivery_partner:
            print("Sign up successful!")
            return True
        else:
            print("Failed to sign up. Please try again.")
    else:
        print("Invalid username or password. Please try again.")
    return False


def restaurant_partner_flow():
    print("1. Sign In")
    print("2. Sign Up")
    auth_choice = input("Enter your choice: ")

    if auth_choice == "1":
        partner = restaurant_partner_login()
        if partner:
            restaurant_partner_menu(partner)
    elif auth_choice == "2":
        if restaurant_partner_signup():
            print("Sign up successful! Please login.")
            partner = restaurant_partner_login()
            if partner:
                restaurant_partner_menu(partner)
    else:
        print("Invalid choice. Please try again.")


def delivery_partner_flow():
    print("1. Sign In")
    print("2. Sign Up")
    auth_choice = input("Enter your choice: ")

    if auth_choice == "1":
        partner = delivery_partner_login()
        if partner:
            delivery_partner_menu(partner)
    elif auth_choice == "2":
        if delivery_partner_signup():
            print("Sign up successful! Please login.")
            partner = delivery_partner_login()
            if partner:
                delivery_partner_menu(partner)


if __name__ == "__main__":
    main()
