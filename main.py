'''
Access all the functions from the other files and build a robust main function. 
Remember to use the functions from the other files to build the main function.
Follow best practices and use the functions from the other files to build the main function.
Refer database.py for the database schema.
Refer validations.py for the validation functions and error messages.

'''

import sqlite3
from menu import Menu
from restaurant import Restaurant
from customer import Customer
from order import Order, OrderItem
from cart import Cart, CartItem
from user import User
from restaurant_partner import RestaurantPartner
from delivery_partner import DeliveryPartner
from membership import Membership
from payment import Payment
from utils.validations import validate_username, validate_password, validate_id, validate_quantity, validate_name, validate_price, validate_description, validate_status
from utils.database import *

DATABASE = 'sprig.db'


def main():
    print("Welcome to Sprig!")
    print("1. Customer")
    print("2. Restaurant Partner")
    print("3. Delivery Partner")
    print("4. Exit")
    choice = input("Enter your role: ")

    if choice == "1":
        customer = customer_login()
        if customer:
            customer_menu(customer)
    elif choice == "2":
        restaurant_partner = restaurant_partner_login()
        if restaurant_partner:
            restaurant_partner_menu(restaurant_partner)
    elif choice == "3":
        delivery_partner = delivery_partner_login()
        if delivery_partner:
            delivery_partner_menu(delivery_partner)
    elif choice == "4":
        print("Thank you for using Sprig!")
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
        print("Invalid username or password. Please try again.")
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
    earnings = delivery_partner.view_earnings()
    if earnings:
        print(f"Earnings: {earnings}")
    else:
        print("No earnings found.")
    delivery_partner_menu(delivery_partner)


if __name__ == "__main__":
    main()
