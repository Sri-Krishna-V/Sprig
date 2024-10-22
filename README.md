# SPRIG

## Overview

The Restaurant Management System is a comprehensive solution designed to manage restaurant operations, including menu management, customer orders, and delivery logistics. This project leverages Python and SQLite to provide a robust backend for handling various aspects of a restaurant's daily operations.

## Features

- **User Management**: Supports different user types including Customers, Restaurant Partners, and Delivery Partners.
- **Restaurant Management**: Allows restaurant partners to manage their restaurant details and menu items.
- **Order Management**: Facilitates order placement, tracking, and payment processing.
- **Delivery Management**: Manages delivery partner assignments and delivery tracking.

## Key Components

### [restaurant.py](restaurant.py)

Defines the `Restaurant` class, which represents restaurant information and menu management.

- **Attributes**:
  - `restaurant_id`: Unique identifier.
  - `name`: Restaurant's name.
  - `address`: Location of the restaurant.

- **Methods**:
  - `get_menu()`: Fetches menu items for display.
  - `get_restaurant_list()`: Returns a list of available restaurants.

### [utils/database.py](utils/database.py)

Handles database initialization and schema creation.

- **Tables**:
  - `Users`: Base table for all users.
  - `Customers`: Extends `Users` for customer-specific details.
  - `RestaurantPartners`: Extends `Users` for restaurant partner-specific details.
  - `DeliveryPartners`: Extends `Users` for delivery partner-specific details.
  - `Restaurants`: Stores restaurant details.
  - `MenuItems`: Stores menu items for each restaurant.
  - `Carts`: Stores cart details for each customer.
  - `CartItems`: Stores items in a cart.

## Getting Started

### Prerequisites

- Python 3.x
- SQLite

## Usage

_**Customers**_: Can browse restaurants, view menus, place orders, and make payments.
_**Restaurant Partners**_: Can manage restaurant details and update menu items.
_**Delivery Partners**_: Can view and manage delivery assignments.

## Contributing

**Contributions are welcome! Please fork the repository and submit a pull request.**

# SPRIG

## Overview

The Restaurant Management System is a comprehensive solution designed to manage restaurant operations, including menu management, customer orders, and delivery logistics. This project leverages Python and SQLite to provide a robust backend for handling various aspects of a restaurant's daily operations.

## Features

- **User Management**: Supports different user types including Customers, Restaurant Partners, and Delivery Partners.
- **Restaurant Management**: Allows restaurant partners to manage their restaurant details and menu items.
- **Order Management**: Facilitates order placement, tracking, and payment processing.
- **Delivery Management**: Manages delivery partner assignments and delivery tracking.

## Key Components

### [restaurant.py](restaurant.py)

Defines the `Restaurant` class, which represents restaurant information and menu management.

- **Attributes**:
  - `restaurant_id`: Unique identifier.
  - `name`: Restaurant's name.
  - `address`: Location of the restaurant.

- **Methods**:
  - `get_menu()`: Fetches menu items for display.
  - `get_restaurant_list()`: Returns a list of available restaurants.

### [utils/database.py](utils/database.py)

Handles database initialization and schema creation.

- **Tables**:
  - `Users`: Base table for all users.
  - `Customers`: Extends `Users` for customer-specific details.
  - `RestaurantPartners`: Extends `Users` for restaurant partner-specific details.
  - `DeliveryPartners`: Extends `Users` for delivery partner-specific details.
  - `Restaurants`: Stores restaurant details.
  - `MenuItems`: Stores menu items for each restaurant.
  - `Carts`: Stores cart details for each customer.
  - `CartItems`: Stores items in a cart.

## Getting Started

### Prerequisites

- Python 3.x
- SQLite

## Usage

_**Customers**_: Can browse restaurants, view menus, place orders, and make payments.
_**Restaurant Partners**_: Can manage restaurant details and update menu items.
_**Delivery Partners**_: Can view and manage delivery assignments.

## Contributing

**Contributions are welcome! Please fork the repository and submit a pull request.**
