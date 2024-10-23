'''

Refer all the files in the project for the complete and accurate code.

'''
import sqlite3
import os

DATABASE = 'sprig.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create Users table (base for all users)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            user_type TEXT NOT NULL CHECK(user_type IN ('Customer', 'RestaurantPartner', 'DeliveryPartner'))
        )
    ''')

    # Create Customers table (extends Users)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customers (
            id INTEGER PRIMARY KEY,
            phone_number TEXT NOT NULL,
            address TEXT,
            FOREIGN KEY (id) REFERENCES Users(id)
        )
    ''')

    # Create RestaurantPartners table (extends Users)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS RestaurantPartners (
            id INTEGER PRIMARY KEY,
            restaurant_id INTEGER NOT NULL,
            address TEXT NOT NULL,
            cuisine_type TEXT NOT NULL,
            FOREIGN KEY (id) REFERENCES Users(id),
            FOREIGN KEY (restaurant_id) REFERENCES Restaurants(id)
        )
    ''')

    # Create DeliveryPartners table (extends Users)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS DeliveryPartners (
            id INTEGER PRIMARY KEY,
            vehicle_type TEXT NOT NULL,
            license_number TEXT NOT NULL,
            FOREIGN KEY (id) REFERENCES Users(id)
        )
    ''')

    # Create index for email in Customers for fast lookups
    cursor.execute(
        'CREATE INDEX IF NOT EXISTS idx_customers_email ON Customers(email)')

    # Create index for restaurant_id in RestaurantPartners for fast lookups
    cursor.execute(
        'CREATE INDEX IF NOT EXISTS idx_restaurant_partners_restaurant_id ON RestaurantPartners(restaurant_id)')

    # Create Restaurants table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_name TEXT NOT NULL,
            address TEXT NOT NULL,
            cuisine_type TEXT NOT NULL,
            rating REAL DEFAULT 0.0
        )
    ''')

    # Create index for restaurant_name in Restaurants for fast searches
    cursor.execute(
        'CREATE INDEX IF NOT EXISTS idx_restaurants_name ON Restaurants(restaurant_name)')

    # Create MenuItems table (each restaurant has multiple menu items)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MenuItems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            item_description TEXT,
            price REAL NOT NULL,
            item_type TEXT NOT NULL,
            availability INTEGER DEFAULT 1,
            FOREIGN KEY (restaurant_id) REFERENCES Restaurants(id)
        )
    ''')

    # Create index for restaurant_id in MenuItems for faster restaurant-menu item lookups
    cursor.execute(
        'CREATE INDEX IF NOT EXISTS idx_menu_items_restaurant_id ON MenuItems(restaurant_id)')

    # Create Carts table (each customer has a cart)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Carts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            total_price REAL DEFAULT 0.0,
            FOREIGN KEY (customer_id) REFERENCES Customers(id)
        )
    ''')

    # Create index for customer_id in Carts for faster lookups
    cursor.execute(
        'CREATE INDEX IF NOT EXISTS idx_carts_customer_id ON Carts(customer_id)')

    # Create CartItems table (to store items in a cart)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CartItems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cart_id INTEGER NOT NULL,
            menu_item_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (cart_id) REFERENCES Carts(id),
            FOREIGN KEY (menu_item_id) REFERENCES MenuItems(id)
        )
    ''')

    # Create index for cart_id in CartItems for fast retrieval of cart contents
    cursor.execute(
        'CREATE INDEX IF NOT EXISTS idx_cart_items_cart_id ON CartItems(cart_id)')

    # Create Orders table (links customers, restaurants, and delivery partners)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            restaurant_id INTEGER NOT NULL,
            order_status TEXT NOT NULL CHECK(order_status IN ('Pending', 'Preparing', 'Out for Delivery', 'Delivered')),
            order_date TEXT NOT NULL,
            delivery_partner_id INTEGER,
            membership_discount REAL DEFAULT 0.0,
            FOREIGN KEY (customer_id) REFERENCES Customers(id),
            FOREIGN KEY (restaurant_id) REFERENCES Restaurants(id),
            FOREIGN KEY (delivery_partner_id) REFERENCES DeliveryPartners(id)
        )
    ''')

    # Create index for customer_id and restaurant_id in Orders for fast lookups
    cursor.execute(
        'CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON Orders(customer_id)')
    cursor.execute(
        'CREATE INDEX IF NOT EXISTS idx_orders_restaurant_id ON Orders(restaurant_id)')

    # Create OrderItems table (each order can have multiple items)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS OrderItems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            menu_item_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (order_id) REFERENCES Orders(id),
            FOREIGN KEY (menu_item_id) REFERENCES MenuItems(id)
        )
    ''')

    # Create index for order_id in OrderItems for fast retrieval of order details
    cursor.execute(
        'CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON OrderItems(order_id)')

    # Create Membership table (each customer can have a membership)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Membership (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            membership_type TEXT NOT NULL,
            discount_rate REAL NOT NULL,
            expiry_date TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES Customers(id)
        )
    ''')

    # Create index for customer_id in Membership for fast membership lookups
    cursor.execute(
        'CREATE INDEX IF NOT EXISTS idx_membership_customer_id ON Membership(customer_id)')

    # Create Payments table (each order has a payment)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            payment_method TEXT NOT NULL,
            payment_status TEXT NOT NULL CHECK(payment_status IN ('Pending', 'Completed', 'Refunded')),
            payment_date TEXT NOT NULL,
            amount REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES Orders(id)
        )
    ''')

    # Create index for order_id in Payments for fast lookup of payments
    cursor.execute(
        'CREATE INDEX IF NOT EXISTS idx_payments_order_id ON Payments(order_id)')

    conn.commit()
    conn.close()


def initialize_database():
    if not os.path.exists(DATABASE):
        create_tables()
        print("Database created and schema initialized.")


# This function will be called when the module is imported
initialize_database()
