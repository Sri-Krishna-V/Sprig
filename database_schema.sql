-- Food Delivery System Database Schema
-- SQLite Database

-- Users Table (Base table for authentication)
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    user_type VARCHAR(20) NOT NULL CHECK(user_type IN ('customer', 'delivery_partner', 'restaurant_owner', 'admin'))
);

-- Customers Table
CREATE TABLE IF NOT EXISTS Customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    customername VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phonenumber VARCHAR(15),
    customer_address TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Restaurant Owners Table
CREATE TABLE IF NOT EXISTS RestaurantOwners (
    ro_id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id INTEGER,
    restaurant_name VARCHAR(100) NOT NULL
);

-- Restaurant Table
CREATE TABLE IF NOT EXISTS Restaurant (
    restaurant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_name VARCHAR(100) NOT NULL,
    restaurant_address TEXT,
    cuisine_type VARCHAR(50),
    rating DECIMAL(2,1) DEFAULT 0.0,
    owner_id INTEGER,
    FOREIGN KEY (owner_id) REFERENCES RestaurantOwners(ro_id)
);

-- Delivery Partners Table
CREATE TABLE IF NOT EXISTS DeliveryPartners (
    d_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(15),
    vehicle_type VARCHAR(50),
    vehicle_number VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Menu Items Table
CREATE TABLE IF NOT EXISTS MenuItems (
    menu_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id INTEGER NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    item_type VARCHAR(20) CHECK(item_type IN ('veg', 'non-veg', 'vegan')),
    availability BOOLEAN DEFAULT 1,
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id) ON DELETE CASCADE
);

-- Membership Table
CREATE TABLE IF NOT EXISTS Membership (
    membership_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER UNIQUE,
    membership_type VARCHAR(20) CHECK(membership_type IN ('basic', 'silver', 'gold', 'platinum')),
    discount_rate DECIMAL(4,2) DEFAULT 0.0,
    expiry_date DATE,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE
);

-- Offers Table
CREATE TABLE IF NOT EXISTS Offers (
    offer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    offer_code VARCHAR(20) UNIQUE NOT NULL,
    description TEXT,
    discount_percentage DECIMAL(4,2),
    valid_from DATE,
    valid_to DATE,
    min_order_amount DECIMAL(10,2)
);

-- Carts Table
CREATE TABLE IF NOT EXISTS Carts (
    cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER UNIQUE,
    totalprice DECIMAL(10,2) DEFAULT 0.0,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE
);

-- Cart Items Table
CREATE TABLE IF NOT EXISTS CartItems (
    cart_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_id INTEGER NOT NULL,
    menu_item_id INTEGER NOT NULL,
    cart_quantity INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (cart_id) REFERENCES Carts(cart_id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES MenuItems(menu_item_id) ON DELETE CASCADE
);

-- Orders Table
CREATE TABLE IF NOT EXISTS Orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    restaurant_id INTEGER NOT NULL,
    delivery_partner_id INTEGER,
    order_status VARCHAR(20) DEFAULT 'pending' CHECK(order_status IN ('pending', 'confirmed', 'preparing', 'out_for_delivery', 'delivered', 'cancelled')),
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    membership_discount DECIMAL(10,2) DEFAULT 0.0,
    total_amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id),
    FOREIGN KEY (delivery_partner_id) REFERENCES DeliveryPartners(d_id)
);

-- Order Items Table
CREATE TABLE IF NOT EXISTS OrderItems (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    menu_item_id INTEGER NOT NULL,
    item_quantity INTEGER NOT NULL DEFAULT 1,
    item_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES MenuItems(menu_item_id)
);

-- Payments Table
CREATE TABLE IF NOT EXISTS Payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER UNIQUE NOT NULL,
    payment_method VARCHAR(20) CHECK(payment_method IN ('cash', 'card', 'upi', 'wallet')),
    payment_status VARCHAR(20) DEFAULT 'pending' CHECK(payment_status IN ('pending', 'completed', 'failed', 'refunded')),
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

-- Create Indexes for better query performance
CREATE INDEX idx_customers_email ON Customers(email);
CREATE INDEX idx_orders_customer ON Orders(customer_id);
CREATE INDEX idx_orders_restaurant ON Orders(restaurant_id);
CREATE INDEX idx_orders_status ON Orders(order_status);
CREATE INDEX idx_menuitems_restaurant ON MenuItems(restaurant_id);
CREATE INDEX idx_orderitems_order ON OrderItems(order_id);
CREATE INDEX idx_payments_order ON Payments(order_id);
