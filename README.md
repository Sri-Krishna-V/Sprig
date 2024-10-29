# 🍽️ SPRIG - Food ordering App

## Overview

The Food Ordering App is a desktop application built using Python and PyQt6 that allows users to browse restaurants, view menus, and place orders for food delivery. The application features a user-friendly interface and provides a seamless experience for customers to order food from their favorite restaurants.

## Features

- **User Authentication**: Users can log in to access the app.
- **Restaurant Browsing**: Users can view a list of available restaurants.
- **Menu Viewing**: Users can view the menu of each restaurant.
- **Cart Management**: Users can add items to their cart, update quantities, and remove items.
- **Checkout Process**: Users can confirm their orders and provide delivery details.
- **Order History**: Orders are saved in a SQLite database for future reference.

## Technologies Used

- **Python**: The programming language used for the application.
- **PyQt6**: A set of Python bindings for the Qt libraries, used for creating the GUI.
- **SQLite**: A lightweight database used to store order information.
- **JSON**: Used for loading restaurant data from a JSON file.

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required packages:

   ```bash
   pip install PyQt6
   ```

3. Ensure you have a `restaurants.json` file in the specified path:

   ```plaintext
   YOUR_PATH\restaurants.json
   ```

## Usage

1. Run the application:

   ```bash
   python main.py
   ```

2. Log in using the provided credentials.
3. Browse through the list of restaurants and view their menus.
4. Add items to your cart and proceed to checkout.
5. Fill in your delivery details and confirm your order.

## Database

The application uses SQLite to store order information. The database file `orders.db` will be created in the same directory as the application if it does not already exist.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs or feature requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the PyQt community for their excellent documentation and support.
- Special thanks to the contributors of the libraries used in this project.
