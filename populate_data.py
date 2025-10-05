import sqlite3
from datetime import datetime, timedelta
import random


def populate_database():
    conn = sqlite3.connect('food_delivery.db')
    cursor = conn.cursor()

    # Execute schema
    with open('database_schema.sql', 'r') as f:
        cursor.executescript(f.read())

    print("Database schema created successfully!")

    # Insert Users
    users_data = [
        ('john_doe', 'pass123', 'customer'),
        ('jane_smith', 'pass123', 'customer'),
        ('mike_wilson', 'pass123', 'customer'),
        ('sarah_jones', 'pass123', 'customer'),
        ('david_brown', 'pass123', 'customer'),
        ('emma_davis', 'pass123', 'customer'),
        ('alex_martin', 'pass123', 'customer'),
        ('lisa_garcia', 'pass123', 'customer'),
        ('driver1', 'pass123', 'delivery_partner'),
        ('driver2', 'pass123', 'delivery_partner'),
        ('driver3', 'pass123', 'delivery_partner'),
        ('driver4', 'pass123', 'delivery_partner'),
        ('driver5', 'pass123', 'delivery_partner'),
    ]
    cursor.executemany(
        'INSERT INTO Users (username, password, user_type) VALUES (?, ?, ?)', users_data)

    # Insert Customers
    customers_data = [
        (1, 'John Doe', 'john.doe@email.com', '9876543210', '123 Main St, City A'),
        (2, 'Jane Smith', 'jane.smith@email.com',
         '9876543211', '456 Oak Ave, City B'),
        (3, 'Mike Wilson', 'mike.wilson@email.com',
         '9876543212', '789 Pine Rd, City A'),
        (4, 'Sarah Jones', 'sarah.jones@email.com',
         '9876543213', '321 Elm St, City C'),
        (5, 'David Brown', 'david.brown@email.com',
         '9876543214', '654 Maple Dr, City B'),
        (6, 'Emma Davis', 'emma.davis@email.com',
         '9876543215', '987 Cedar Ln, City A'),
        (7, 'Alex Martin', 'alex.martin@email.com',
         '9876543216', '147 Birch Ave, City C'),
        (8, 'Lisa Garcia', 'lisa.garcia@email.com',
         '9876543217', '258 Willow St, City B'),
    ]
    cursor.executemany(
        'INSERT INTO Customers (user_id, customername, email, phonenumber, customer_address) VALUES (?, ?, ?, ?, ?)', customers_data)

    # Insert Restaurant Owners
    owners_data = [
        (None, 'Pizza Palace Owner'),
        (None, 'Burger Hub Owner'),
        (None, 'Sushi Express Owner'),
        (None, 'Taco Fiesta Owner'),
        (None, 'Pasta House Owner'),
        (None, 'Indian Spice Owner'),
    ]
    cursor.executemany(
        'INSERT INTO RestaurantOwners (restaurant_id, restaurant_name) VALUES (?, ?)', owners_data)

    # Insert Restaurants
    restaurants_data = [
        ('Pizza Palace', '100 Food Court, City A', 'Italian', 4.5, 1),
        ('Burger Hub', '200 Downtown, City B', 'American', 4.2, 2),
        ('Sushi Express', '300 Market St, City A', 'Japanese', 4.7, 3),
        ('Taco Fiesta', '400 Main Ave, City C', 'Mexican', 4.3, 4),
        ('Pasta House', '500 Plaza Rd, City B', 'Italian', 4.6, 5),
        ('Indian Spice', '600 Temple St, City A', 'Indian', 4.4, 6),
    ]
    cursor.executemany(
        'INSERT INTO Restaurant (restaurant_name, restaurant_address, cuisine_type, rating, owner_id) VALUES (?, ?, ?, ?, ?)', restaurants_data)

    # Insert Delivery Partners
    delivery_data = [
        (9, 'Raj Kumar', '9998887770', 'Bike', 'DL01AB1234'),
        (10, 'Amit Singh', '9998887771', 'Scooter', 'DL02CD5678'),
        (11, 'Priya Sharma', '9998887772', 'Bike', 'DL03EF9012'),
        (12, 'Vikram Patel', '9998887773', 'Scooter', 'DL04GH3456'),
        (13, 'Neha Reddy', '9998887774', 'Bike', 'DL05IJ7890'),
    ]
    cursor.executemany(
        'INSERT INTO DeliveryPartners (user_id, name, phone_number, vehicle_type, vehicle_number) VALUES (?, ?, ?, ?, ?)', delivery_data)

    # Insert Menu Items for each restaurant
    menu_items = [
        # Pizza Palace (restaurant_id = 1)
        (1, 'Margherita Pizza', 'Classic tomato and mozzarella', 299.00, 'veg', 1),
        (1, 'Pepperoni Pizza', 'Loaded with pepperoni', 399.00, 'non-veg', 1),
        (1, 'Veggie Supreme Pizza', 'Mixed vegetables with cheese', 349.00, 'veg', 1),
        (1, 'Garlic Bread', 'Toasted garlic bread', 99.00, 'veg', 1),

        # Burger Hub (restaurant_id = 2)
        (2, 'Classic Burger', 'Beef patty with lettuce and tomato', 199.00, 'non-veg', 1),
        (2, 'Veggie Burger', 'Plant-based patty', 179.00, 'veg', 1),
        (2, 'Cheese Burger', 'Double cheese delight', 249.00, 'non-veg', 1),
        (2, 'French Fries', 'Crispy golden fries', 89.00, 'veg', 1),

        # Sushi Express (restaurant_id = 3)
        (3, 'California Roll', 'Crab, avocado, cucumber', 399.00, 'non-veg', 1),
        (3, 'Vegetable Roll', 'Mixed veggies wrapped in seaweed', 299.00, 'veg', 1),
        (3, 'Salmon Nigiri', 'Fresh salmon on rice', 449.00, 'non-veg', 1),
        (3, 'Miso Soup', 'Traditional Japanese soup', 149.00, 'veg', 1),

        # Taco Fiesta (restaurant_id = 4)
        (4, 'Chicken Tacos', 'Grilled chicken with salsa', 249.00, 'non-veg', 1),
        (4, 'Bean Burritos', 'Black beans and rice wrapped', 199.00, 'veg', 1),
        (4, 'Nachos Supreme', 'Loaded nachos with cheese', 279.00, 'veg', 1),
        (4, 'Guacamole Dip', 'Fresh avocado dip', 129.00, 'vegan', 1),

        # Pasta House (restaurant_id = 5)
        (5, 'Alfredo Pasta', 'Creamy white sauce pasta', 299.00, 'veg', 1),
        (5, 'Bolognese Pasta', 'Meat sauce pasta', 349.00, 'non-veg', 1),
        (5, 'Penne Arrabiata', 'Spicy tomato sauce', 279.00, 'veg', 1),
        (5, 'Caesar Salad', 'Fresh romaine with dressing', 199.00, 'veg', 1),

        # Indian Spice (restaurant_id = 6)
        (6, 'Butter Chicken', 'Creamy tomato curry with chicken', 349.00, 'non-veg', 1),
        (6, 'Paneer Tikka Masala', 'Cottage cheese in rich gravy', 299.00, 'veg', 1),
        (6, 'Biryani (Veg)', 'Aromatic rice with vegetables', 249.00, 'veg', 1),
        (6, 'Biryani (Chicken)', 'Aromatic rice with chicken', 299.00, 'non-veg', 1),
        (6, 'Naan Bread', 'Tandoor-baked bread', 49.00, 'veg', 1),
    ]
    cursor.executemany(
        'INSERT INTO MenuItems (restaurant_id, item_name, description, price, item_type, availability) VALUES (?, ?, ?, ?, ?, ?)', menu_items)

    # Insert Memberships
    membership_data = [
        (1, 'gold', 10.00, (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')),
        (2, 'silver', 5.00, (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d')),
        (3, 'platinum', 15.00, (datetime.now() +
         timedelta(days=365)).strftime('%Y-%m-%d')),
        (4, 'basic', 0.00, (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')),
        (5, 'silver', 5.00, (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d')),
    ]
    cursor.executemany(
        'INSERT INTO Membership (customer_id, membership_type, discount_rate, expiry_date) VALUES (?, ?, ?, ?)', membership_data)

    # Insert Offers
    offers_data = [
        ('FIRST50', '50% off on first order',
         50.00, '2025-01-01', '2025-12-31', 200.00),
        ('SAVE20', 'Flat 20% off', 20.00, '2025-01-01', '2025-06-30', 300.00),
        ('FREESHIP', 'Free delivery', 0.00, '2025-01-01', '2025-12-31', 150.00),
        ('WEEKEND30', '30% off on weekends', 30.00,
         '2025-01-01', '2025-12-31', 400.00),
    ]
    cursor.executemany(
        'INSERT INTO Offers (offer_code, description, discount_percentage, valid_from, valid_to, min_order_amount) VALUES (?, ?, ?, ?, ?, ?)', offers_data)

    # Insert some historical orders
    orders_data = [
        (1, 1, 1, 'delivered', (datetime.now() - timedelta(days=5)
                                ).strftime('%Y-%m-%d %H:%M:%S'), 29.90, 598.00),
        (2, 2, 2, 'delivered', (datetime.now() - timedelta(days=4)
                                ).strftime('%Y-%m-%d %H:%M:%S'), 0.00, 378.00),
        (3, 3, 3, 'delivered', (datetime.now() - timedelta(days=3)
                                ).strftime('%Y-%m-%d %H:%M:%S'), 74.85, 748.50),
        (1, 1, 4, 'delivered', (datetime.now() - timedelta(days=2)
                                ).strftime('%Y-%m-%d %H:%M:%S'), 34.90, 698.00),
        (4, 4, 5, 'delivered', (datetime.now() - timedelta(days=1)
                                ).strftime('%Y-%m-%d %H:%M:%S'), 0.00, 549.00),
        (5, 5, 1, 'out_for_delivery', datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S'), 17.45, 349.00),
        (6, 6, 2, 'preparing', datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S'), 0.00, 448.00),
        (7, 3, 3, 'confirmed', datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S'), 0.00, 299.00),
    ]
    cursor.executemany(
        'INSERT INTO Orders (customer_id, restaurant_id, delivery_partner_id, order_status, order_date, membership_discount, total_amount) VALUES (?, ?, ?, ?, ?, ?, ?)', orders_data)

    # Insert Order Items
    order_items_data = [
        (1, 1, 2, 299.00),
        (1, 4, 1, 99.00),
        (1, 2, 1, 199.00),
        (2, 5, 1, 199.00),
        (2, 8, 2, 89.00),
        (3, 9, 1, 399.00),
        (3, 11, 1, 449.00),
        (4, 1, 1, 299.00),
        (4, 2, 1, 399.00),
        (5, 17, 1, 299.00),
        (5, 19, 1, 279.00),
        (6, 13, 1, 249.00),
        (6, 14, 1, 199.00),
        (7, 6, 2, 179.00),
        (7, 8, 3, 89.00),
        (8, 10, 1, 299.00),
    ]
    cursor.executemany(
        'INSERT INTO OrderItems (order_id, menu_item_id, item_quantity, item_price) VALUES (?, ?, ?, ?)', order_items_data)

    # Insert Payments
    payments_data = [
        (1, 'upi', 'completed', (datetime.now() -
         timedelta(days=5)).strftime('%Y-%m-%d %H:%M:%S'), 598.00),
        (2, 'card', 'completed', (datetime.now() -
         timedelta(days=4)).strftime('%Y-%m-%d %H:%M:%S'), 378.00),
        (3, 'upi', 'completed', (datetime.now() -
         timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S'), 748.50),
        (4, 'wallet', 'completed', (datetime.now() -
         timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S'), 698.00),
        (5, 'cash', 'completed', (datetime.now() -
         timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'), 549.00),
        (6, 'upi', 'pending', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 349.00),
        (7, 'card', 'pending', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 448.00),
        (8, 'cash', 'pending', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 299.00),
    ]
    cursor.executemany(
        'INSERT INTO Payments (order_id, payment_method, payment_status, payment_date, amount) VALUES (?, ?, ?, ?, ?)', payments_data)

    # Insert some carts
    carts_data = [
        (8, 449.00),
    ]
    cursor.executemany(
        'INSERT INTO Carts (customer_id, totalprice) VALUES (?, ?)', carts_data)

    # Insert cart items
    cart_items_data = [
        (1, 22, 1),
        (1, 25, 1),
    ]
    cursor.executemany(
        'INSERT INTO CartItems (cart_id, menu_item_id, cart_quantity) VALUES (?, ?, ?)', cart_items_data)

    conn.commit()
    print("Sample data inserted successfully!")
    print(f"Total records inserted:")
    print(f"  - Users: {len(users_data)}")
    print(f"  - Customers: {len(customers_data)}")
    print(f"  - Restaurants: {len(restaurants_data)}")
    print(f"  - Menu Items: {len(menu_items)}")
    print(f"  - Orders: {len(orders_data)}")
    print(f"  - Delivery Partners: {len(delivery_data)}")

    conn.close()


if __name__ == '__main__':
    populate_database()
