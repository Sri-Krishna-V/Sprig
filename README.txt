Overview of Sprig

Sprig is a software system designed to simulate a food delivery platform similar to Zomato, incorporating customers, restaurants, delivery partners, orders, and payments. The project is built using Python and uses SQLite3 for database management. The design is modular, with each class responsible for a specific part of the system, making the codebase maintainable and scalable.

The primary focus of Sprig is to streamline interactions between different users of the system: customers, restaurant partners, and delivery partners, while managing orders, memberships, payments, and deliveries efficiently. Each part of the system is built to follow best coding practices, including error handling, validation, and modular design.

Key Concepts
User Interactions:

Customers can browse restaurants, view menus, add items to their cart, and place orders.
Restaurant partners manage their restaurant’s menu, view orders, and update order statuses.
Delivery partners handle the delivery process by accepting assigned orders and updating their status.
Membership System:

Customers can subscribe to a membership for special discounts.
Membership benefits affect both customers (through discounted prices) and restaurant partners (by attracting more orders).
Database Management:

Uses SQLite3 to store information about users, orders, menus, and payments.
Follows best practices for relational databases, using foreign keys for relationships between entities.
Modular Code Structure:

Each component of the system is implemented in a separate file for ease of development and maintenance.
utils folder contains helper files like database.py for database operations and validations.py for input validation.
Detailed Structure
main.py
Purpose: Acts as the entry point for the application.
Responsibilities: Initializes the application, establishes database connections, and manages the user interface or command-line interactions.
user.py
Classes: User (parent class).
Purpose: Manages common attributes and methods for all types of users.
Attributes:
user_id: Unique identifier for each user.
name: Name of the user.
email: Email address of the user.
Methods:
login(): Validates user credentials.
logout(): Ends user session.
customer.py
Class: Customer (inherits from User).
Purpose: Represents customers and their interactions with the platform.
Attributes:
customer_id: Unique identifier.
Methods:
view_restaurants(): Displays a list of available restaurants.
view_menu(): Displays the menu of a specific restaurant.
place_order(): Places an order based on cart items.
restaurant_partner.py
Class: RestaurantPartner (inherits from User).
Purpose: Represents restaurant partners managing their restaurant.
Attributes:
partner_id: Unique identifier.
restaurant_id: Associated restaurant ID.
Methods:
view_orders(): Retrieves all orders for the restaurant.
update_order_status(): Updates the status of a specific order (e.g., Preparing, Ready).
delivery_partner.py
Class: DeliveryPartner (inherits from User).
Purpose: Manages delivery-related operations.
Attributes:
partner_id: Unique identifier.
Methods:
view_assigned_orders(): Lists orders assigned to the delivery partner.
update_order_status(): Updates the delivery status (e.g., In Transit, Delivered).
restaurant.py
Class: Restaurant.
Purpose: Represents a restaurant's data and operations.
Attributes:
restaurant_id: Unique identifier.
Methods:
get_menu(): Fetches the restaurant's menu.
get_restaurant_list(): Returns all available restaurants.
cart.py
Class: Cart.
Purpose: Manages items selected by customers.
Attributes:
customer_id: Associated customer.
Methods:
add_item(): Adds an item to the cart.
remove_item(): Removes an item from the cart.
view_cart(): Retrieves all items in the cart.
order.py
Classes: Order, OrderItem.
Purpose: Manages order creation and details.
Attributes:
order_id: Unique identifier.
customer_id: Associated customer.
restaurant_id: Restaurant fulfilling the order.
Methods:
place_order(): Places an order with all cart items.
get_order_details(): Retrieves details of a specific order.
menu.py
Classes: Menu, MenuItem.
Purpose: Manages menu items for a restaurant.
Attributes:
restaurant_id: Associated restaurant.
Methods:
add_menu_item(): Adds a new item to the menu.
remove_menu_item(): Removes an item from the menu.
get_menu(): Retrieves the full menu.
membership.py
Class: Membership.
Purpose: Manages the membership system for customers.
Attributes:
customer_id: Associated customer.
Methods:
check_membership_status(): Checks if a customer is a member.
apply_membership_discount(): Applies a discount to the total order value.
payment.py
Class: Payment.
Purpose: Handles payments for orders.
Attributes:
order_id: Associated order.
Methods:
process_payment(): Processes payment for a given order.
utils/database.py
Purpose: Handles all database operations.
Methods:
connect(): Establishes a connection to the SQLite database.
execute_query(): Executes read/write queries.
close(): Closes the database connection.
utils/validations.py
Purpose: Provides input validation functions to ensure data integrity.
Methods:
validate_email(): Checks if the email format is correct.
validate_order_status(): Ensures that the order status is valid.
validate_menu_item(): Validates the existence of a menu item in the database.
Flow of the System
Customer Browses Restaurants:

Customer uses view_restaurants() to see available options.
Chooses a restaurant and calls view_menu() to see items.
Adding to Cart:

Customer adds menu items to their Cart using add_item().
Placing an Order:

The place_order() method in Order takes items from the cart and creates a new order entry in the database.
OrderItems are created for each menu item added.
Restaurant Prepares Order:

RestaurantPartner views incoming orders using view_orders().
Updates the order status using update_order_status().
Delivery Partner Picks Up Order:

DeliveryPartner checks assigned orders with view_assigned_orders() and updates the status using update_order_status() (e.g., In Transit).
Payment Processing:

Payment processes the payment through process_payment() after order completion.
Membership discounts are applied if applicable.
Order Completion:

The order is marked as Delivered, and the transaction is completed.
Summary
Sprig's modular approach allows for an organized codebase, making it easier to extend or maintain each part of the system. By dividing the logic across different classes and files, each component is manageable and testable individually. The use of SQLite3 provides a simple yet powerful way to store and retrieve data for the application's needs, while maintaining relationships between customers, restaurants, and orders.