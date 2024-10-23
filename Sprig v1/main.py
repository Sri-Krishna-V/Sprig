import sys
import json
import sqlite3
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QTabWidget, QScrollArea, QLineEdit,
                             QMessageBox, QDialog, QDialogButtonBox, QSpinBox, QTabBar)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QGuiApplication
from login import LoginDialog
from animated_widgets import SlidingStackedWidget


class Restaurant:
    def __init__(self, name, menu):
        self.name = name
        self.menu = menu


class Order:
    def __init__(self, restaurant, items, total, customer_name, address):
        self.restaurant = restaurant
        self.items = items
        self.total = total
        self.customer_name = customer_name
        self.address = address
        self.timestamp = datetime.now()


class FoodOrderingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Food Ordering App")
        self.showFullScreen()

        self.style_dict = {
            'primary_color': '#2ECC71',
            'secondary_color': '#27AE60',
            'text_dark': '#2C3E50',
            'text_light': '#7F8C8D',
            'background': '#FFFFFF',
            'card_background': '#F8F9FA',
            'common_styles': """
                QWidget {
                    font-family: 'Arial';
                    background-color: white;
                }
                QPushButton {
                    background-color: #2ECC71;
                    color: white;
                    border: none;
                    padding: 10px;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 5px;
                    min-width: 100px;
                }
                QPushButton:hover {
                    background-color: #27AE60;
                }
                QPushButton:pressed {
                    background-color: #219A52;
                }
                QLabel {
                    color: #2C3E50;
                }
                QSpinBox {
                    padding: 5px;
                    border: 1px solid #BDC3C7;
                    border-radius: 3px;
                }
            """
        }

        self.restaurants = self.load_restaurants()
        self.cart = []
        self.user_data = None

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Replace QTabWidget with custom widget
        self.tab_widget = SlidingStackedWidget()
        self.tab_bar = QTabBar()
        self.tab_bar.currentChanged.connect(self._handle_tab_change)
        self.layout.addWidget(self.tab_bar)
        self.layout.addWidget(self.tab_widget)

        self.show_login_dialog()

    def _handle_tab_change(self, index):
        self.tab_widget.slideIn(index)

    def show_login_dialog(self):
        login_dialog = LoginDialog()
        login_dialog.login_successful.connect(self.on_login_successful)
        if login_dialog.exec():
            self.create_home_page()
            self.create_restaurant_page()
            self.create_cart_page()
        else:
            sys.exit()

    def on_login_successful(self, user_data):
        self.user_data = user_data
        QMessageBox.information(self, "Login Successful",
                                f"Welcome, {user_data['name']}!")

    def load_restaurants(self):
        try:
            with open(r'C:\Users\srikr\Desktop\Studies\Sem 3\OOPs by Python\Project\Sprig\Sprig v1\restaurants.json', 'r') as f:
                data = json.load(f)
                return [Restaurant(r['name'], r['menu']) for r in data]
        except FileNotFoundError:
            QMessageBox.critical(
                self, "Error", "Restaurants data file not found.")
            return []
        except json.JSONDecodeError:
            QMessageBox.critical(
                self, "Error", "Invalid restaurants data file.")
            return []

    def create_home_page(self):
        home_page = QWidget()
        layout = QVBoxLayout(home_page)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 40, 30, 40)

        # App Logo/Banner
        logo_label = QLabel("🍽️ SPRIG")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("""
            font-size: 48px;
            font-weight: bold;
            color: #2ECC71;
            margin: 20px;
            font-family: 'Arial Black';
        """)
        layout.addWidget(logo_label)

        # Welcome Message
        welcome_label = QLabel("Welcome to Food Ordering App")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #34495E;
            margin: 10px;
        """)
        layout.addWidget(welcome_label)

        # Tagline
        tagline_label = QLabel("Delicious food at your doorstep!")
        tagline_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tagline_label.setStyleSheet("""
            font-size: 18px;
            color: #7F8C8D;
            font-style: italic;
            margin-bottom: 30px;
        """)
        layout.addWidget(tagline_label)

        # Features Container
        features_widget = QWidget()
        features_layout = QHBoxLayout(features_widget)
        features_layout.setSpacing(15)

        # Feature Cards
        feature_styles = """
            QWidget {
                background-color: #F8F9FA;
                border-radius: 10px;
                padding: 15px;
            }
            QLabel {
                font-size: 16px;
                color: #2C3E50;
            }
        """

        # Feature 1
        feature1 = QWidget()
        feature1.setStyleSheet(feature_styles)
        f1_layout = QVBoxLayout(feature1)
        f1_layout.addWidget(QLabel("🚀 Quick Delivery"))
        f1_layout.addWidget(QLabel("30 mins or free!"))
        features_layout.addWidget(feature1)

        # Feature 2
        feature2 = QWidget()
        feature2.setStyleSheet(feature_styles)
        f2_layout = QVBoxLayout(feature2)
        f2_layout.addWidget(QLabel("🌟 Best Restaurants"))
        f2_layout.addWidget(QLabel("Curated selection"))
        features_layout.addWidget(feature2)

        # Feature 3
        feature3 = QWidget()
        feature3.setStyleSheet(feature_styles)
        f3_layout = QVBoxLayout(feature3)
        f3_layout.addWidget(QLabel("💫 Great Offers"))
        f3_layout.addWidget(QLabel("Amazing discounts"))
        features_layout.addWidget(feature3)

        layout.addWidget(features_widget)

        # Browse Button with enhanced styling
        browse_button = QPushButton("Browse Restaurants")
        browse_button.setStyleSheet("""
            QPushButton {
                background-color: #2ECC71;
                color: white;
                border: none;
                padding: 15px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 8px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #27AE60;
            }
            QPushButton:pressed {
                background-color: #219A52;
            }
        """)
        browse_button.setCursor(Qt.CursorShape.PointingHandCursor)
        browse_button.clicked.connect(
            lambda: self._handle_tab_change(1))

        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.addStretch()
        button_layout.addWidget(browse_button)
        button_layout.addStretch()
        layout.addWidget(button_container)

        # Add some stretch to push everything up
        layout.addStretch()

        # Set the background color for the entire home page
        home_page.setStyleSheet("""
            QWidget {
                background-color: white;
            }
        """)

        self.tab_widget.addWidget(home_page)
        self.tab_bar.addTab("Home")

    def create_restaurant_page(self):
        restaurant_page = QWidget()
        layout = QVBoxLayout(restaurant_page)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Header
        header = QLabel("Our Restaurants")
        header.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #2ECC71;
            margin-bottom: 20px;
        """)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }
            QScrollBar:vertical {
                border: none;
                background: #F8F9FA;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #2ECC71;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(15)

        for restaurant in self.restaurants:
            frame = QWidget()
            frame.setStyleSheet("""
                QWidget {
                    background-color: #F8F9FA;
                    border-radius: 10px;
                    padding: 10px;
                }
                QWidget:hover {
                    background-color: #ECF0F1;
                }
            """)
            frame_layout = QHBoxLayout(frame)
            frame_layout.setSpacing(15)

            # Restaurant icon (you can replace with actual restaurant images)
            icon = QLabel("🍽️")
            icon.setStyleSheet("font-size: 24px;")
            frame_layout.addWidget(icon)

            # Restaurant details
            details_widget = QWidget()
            details_layout = QVBoxLayout(details_widget)

            name_label = QLabel(restaurant.name)
            name_label.setStyleSheet(
                "font-size: 18px; font-weight: bold; color: #2C3E50;")
            details_layout.addWidget(name_label)

            frame_layout.addWidget(details_widget)
            frame_layout.addStretch()

            view_menu_button = QPushButton("View Menu")
            view_menu_button.setCursor(Qt.CursorShape.PointingHandCursor)
            view_menu_button.setStyleSheet("""
                QPushButton {
                    background-color: #2ECC71;
                    color: white;
                    border: none;
                    padding: 8px 15px;
                    border-radius: 5px;
                    font-weight: bold;
                    min-width: 100px;
                    margin: 5px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #27AE60;
                }
                QPushButton:pressed {
                    background-color: #219A52;
                }
            """)
            view_menu_button.clicked.connect(
                lambda checked, r=restaurant: self.show_menu(r))
            frame_layout.addWidget(view_menu_button)

            scroll_layout.addWidget(frame)

        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)

        self.tab_widget.addWidget(restaurant_page)
        self.tab_bar.addTab("Restaurants")

    def show_menu(self, restaurant):
        menu_dialog = QDialog(self)
        menu_dialog.setWindowTitle(f"{restaurant.name} Menu")
        menu_dialog.setWindowFlags(
            Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        menu_dialog.showFullScreen()

        # Set the background gradient for the entire dialog
        menu_dialog.setStyleSheet("""
            QDialog {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #E8F5E9, stop: 1 #F1F8E9
                );
            }
            QScrollArea {
                background: transparent;
            }
            QWidget {
                background: transparent;
            }
        """)

        layout = QVBoxLayout(menu_dialog)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Header with updated style
        header = QLabel(f"{restaurant.name} Menu")
        header.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #2ECC71;
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.7);
        """)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: rgba(46, 204, 113, 0.1);
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #2ECC71;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(15)

        for item, details in restaurant.menu.items():
            frame = QWidget()
            frame.setStyleSheet("""
                QWidget {
                    background-color: rgba(255, 255, 255, 0.85);
                    border-radius: 10px;
                    padding: 15px;
                }
                QWidget:hover {
                    background-color: rgba(255, 255, 255, 0.95);
                    border: 1px solid #2ECC71;
                }
            """)
            frame_layout = QHBoxLayout(frame)
            frame_layout.setSpacing(15)

            # Item details
            details_widget = QWidget()
            details_layout = QVBoxLayout(details_widget)

            item_name = QLabel(item)
            item_name.setStyleSheet("""
                font-size: 16px;
                font-weight: bold;
                color: #2C3E50;
            """)
            details_layout.addWidget(item_name)

            price_label = QLabel(f"Rs.{details['price']}")
            price_label.setStyleSheet("""
                color: #27AE60;
                font-weight: bold;
                font-size: 14px;
            """)
            details_layout.addWidget(price_label)

            desc_label = QLabel(details['description'])
            desc_label.setStyleSheet("""
                color: #7F8C8D;
                font-size: 12px;
            """)
            desc_label.setWordWrap(True)
            details_layout.addWidget(desc_label)

            frame_layout.addWidget(details_widget)
            frame_layout.addStretch()

            # Quantity and Add section
            controls_widget = QWidget()
            controls_layout = QHBoxLayout(controls_widget)

            minus_button = QPushButton("-")
            minus_button.setFixedSize(30, 30)
            minus_button.setStyleSheet("""
                QPushButton {
                    background-color: #E74C3C;
                    color: white;
                    border: none;
                    border-radius: 15px;
                    font-weight: bold;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #C0392B;
                }
            """)
            controls_layout.addWidget(minus_button)

            qty_spinbox = QSpinBox()
            qty_spinbox.setMinimum(0)
            qty_spinbox.setMaximum(10)
            qty_spinbox.setStyleSheet("""
                QSpinBox {
                    background-color: white;
                    color: #2C3E50;
                    padding: 5px;
                    border: 1px solid #BDC3C7;
                    border-radius: 3px;
                    min-width: 70px;
                }
            """)
            controls_layout.addWidget(qty_spinbox)

            plus_button = QPushButton("+")
            plus_button.setFixedSize(30, 30)
            plus_button.setStyleSheet("""
                QPushButton {
                    background-color: #2ECC71;
                    color: white;
                    border: none;
                    border-radius: 15px;
                    font-weight: bold;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #27AE60;
                }
            """)
            controls_layout.addWidget(plus_button)

            minus_button.clicked.connect(
                lambda _, sb=qty_spinbox: sb.setValue(sb.value() - 1))
            plus_button.clicked.connect(
                lambda _, sb=qty_spinbox: sb.setValue(sb.value() + 1))

            add_button = QPushButton("Add")
            add_button.setCursor(Qt.CursorShape.PointingHandCursor)
            add_button.setStyleSheet("""
                QPushButton {
                    background-color: #2ECC71;
                    color: white;
                    border: none;
                    padding: 8px 15px;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #27AE60;
                }
                QPushButton:pressed {
                    background-color: #219A52;
                }
            """)
            add_button.clicked.connect(
                lambda checked, r=restaurant, i=item, d=details, q=qty_spinbox:
                self.add_to_cart(r, i, d, q.value())
            )
            controls_layout.addWidget(add_button)

            frame_layout.addWidget(controls_widget)
            scroll_layout.addWidget(frame)

        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)

        # Close button
        close_button = QPushButton("Close")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                padding: 12px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        close_button.clicked.connect(menu_dialog.accept)
        layout.addWidget(close_button)

        menu_dialog.setStyleSheet(self.style_dict['common_styles'])
        menu_dialog.exec()

    def add_to_cart(self, restaurant, item, details, quantity):
        if quantity > 0:
            for _ in range(quantity):
                self.cart.append((restaurant, item, details))
            QMessageBox.information(self, "Added to Cart", f"{quantity} {
                                    item}(s) has been added to your cart.")
            self.update_cart_page()

    def create_cart_page(self):
        self.cart_page = QWidget()
        self.cart_layout = QVBoxLayout(self.cart_page)
        self.cart_layout.setSpacing(20)
        self.cart_layout.setContentsMargins(30, 30, 30, 30)

        # Header
        header = QLabel("Your Cart")
        header.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #2ECC71;
            margin-bottom: 20px;
        """)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cart_layout.addWidget(header)

        # Cart items container
        self.cart_items_widget = QWidget()
        self.cart_items_layout = QVBoxLayout(self.cart_items_widget)
        self.cart_items_layout.setSpacing(15)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }
            QScrollBar:vertical {
                border: none;
                background: #F8F9FA;
                width: 10px;
                margin: 0px;
            }
        """)
        scroll_area.setWidget(self.cart_items_widget)
        self.cart_layout.addWidget(scroll_area)

        # Checkout button
        self.checkout_button = QPushButton("Proceed to Checkout")
        self.checkout_button.setStyleSheet("""
            QPushButton {
                padding: 15px;
                font-size: 18px;
                min-width: 200px;
            }
        """)
        self.checkout_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.checkout_button.clicked.connect(self.checkout)

        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.addStretch()
        button_layout.addWidget(self.checkout_button)
        button_layout.addStretch()
        self.cart_layout.addWidget(button_container)

        self.cart_page.setStyleSheet(self.style_dict['common_styles'])
        self.tab_widget.addWidget(self.cart_page)
        self.tab_bar.addTab("Cart")

        self.update_cart_page()

    def update_cart_page(self):
        for i in reversed(range(self.cart_items_layout.count())):
            self.cart_items_layout.itemAt(i).widget().setParent(None)

        if not self.cart:
            empty_label = QLabel("Your cart is empty")
            empty_label.setStyleSheet("font-size: 18px;")
            self.cart_items_layout.addWidget(empty_label)
            self.checkout_button.setEnabled(False)
        else:
            self.checkout_button.setEnabled(True)
            cart_items = {}
            for restaurant, item, details in self.cart:
                if (restaurant, item) not in cart_items:
                    cart_items[(restaurant, item)] = {
                        'details': details, 'quantity': 1}
                else:
                    cart_items[(restaurant, item)]['quantity'] += 1

            for (restaurant, item), item_data in cart_items.items():
                frame = QWidget()
                frame_layout = QHBoxLayout(frame)

                label = QLabel(
                    f"{item} - Rs.{item_data['details']['price']} x {item_data['quantity']}")
                frame_layout.addWidget(label)

                minus_button = QPushButton("-")
                minus_button.setFixedSize(30, 30)
                minus_button.setStyleSheet("""
                    QPushButton {
                        background-color: #E74C3C;
                        color: white;
                        border: none;
                        border-radius: 15px;
                        font-weight: bold;
                        font-size: 16px;
                    }
                    QPushButton:hover {
                        background-color: #C0392B;
                    }
                """)
                frame_layout.addWidget(minus_button)

                qty_spinbox = QSpinBox()
                qty_spinbox.setMinimum(0)
                qty_spinbox.setMaximum(10)
                qty_spinbox.setValue(item_data['quantity'])
                qty_spinbox.setStyleSheet("""
                    QSpinBox {
                        background-color: white;
                        color: #2C3E50;
                        padding: 5px;
                        border: 1px solid #BDC3C7;
                        border-radius: 3px;
                        min-width: 70px;
                    }
                """)
                frame_layout.addWidget(qty_spinbox)

                plus_button = QPushButton("+")
                plus_button.setFixedSize(30, 30)
                plus_button.setStyleSheet("""
                    QPushButton {
                        background-color: #2ECC71;
                        color: white;
                        border: none;
                        border-radius: 15px;
                        font-weight: bold;
                        font-size: 16px;
                    }
                    QPushButton:hover {
                        background-color: #27AE60;
                    }
                """)
                frame_layout.addWidget(plus_button)

                minus_button.clicked.connect(
                    lambda _, sb=qty_spinbox: sb.setValue(sb.value() - 1))
                plus_button.clicked.connect(
                    lambda _, sb=qty_spinbox: sb.setValue(sb.value() + 1))

                qty_spinbox.valueChanged.connect(
                    lambda value, r=restaurant, i=item, d=item_data['details']: self.update_cart_quantity(r, i, d, value))

                remove_button = QPushButton("Remove")
                remove_button.clicked.connect(
                    lambda checked, r=restaurant, i=item: self.remove_from_cart(r, i))
                frame_layout.addWidget(remove_button)

                self.cart_items_layout.addWidget(frame)

    def update_cart_quantity(self, restaurant, item, details, new_quantity):
        self.cart = [x for x in self.cart if not (
            x[0] == restaurant and x[1] == item)]
        for _ in range(new_quantity):
            self.cart.append((restaurant, item, details))
        self.update_cart_page()

    def remove_from_cart(self, restaurant, item):
        self.cart = [x for x in self.cart if not (
            x[0] == restaurant and x[1] == item)]
        self.update_cart_page()

    def checkout(self):
        checkout_dialog = QDialog(self)
        checkout_dialog.setWindowTitle("Checkout")
        checkout_dialog.setWindowFlags(
            Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        checkout_dialog.showFullScreen()

        layout = QVBoxLayout(checkout_dialog)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Header
        header = QLabel("Order Summary")
        header.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #2ECC71;
            margin-bottom: 20px;
        """)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        # Order items
        items_widget = QWidget()
        items_widget.setStyleSheet("""
            QWidget {
                background-color: #F8F9FA;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        items_layout = QVBoxLayout(items_widget)

        cart_items = {}
        total = 0
        for restaurant, item, details in self.cart:
            if (restaurant, item) not in cart_items:
                cart_items[(restaurant, item)] = {
                    'details': details,
                    'quantity': self.cart.count((restaurant, item, details))
                }
                total += details['price'] * \
                    cart_items[(restaurant, item)]['quantity']

        for (restaurant, item), item_data in cart_items.items():
            item_label = QLabel(
                f"{item} x{
                    item_data['quantity']} - Rs.{item_data['details']['price'] * item_data['quantity']}"
            )
            item_label.setStyleSheet("font-size: 14px; margin: 5px;")
            items_layout.addWidget(item_label)

        total_label = QLabel(f"Total: Rs.{total}")
        total_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #2ECC71; margin-top: 10px;")
        items_layout.addWidget(total_label)
        layout.addWidget(items_widget)

        # Delivery details
        delivery_widget = QWidget()
        delivery_widget.setStyleSheet("""
            QWidget {
                background-color: #F8F9FA;
                border-radius: 10px;
                padding: 20px;
            }
            QLabel {
                font-size: 14px;
                margin-bottom: 5px;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #BDC3C7;
                border-radius: 4px;
                margin-bottom: 15px;
            }
        """)
        delivery_layout = QVBoxLayout(delivery_widget)

        delivery_layout.addWidget(QLabel("Name:"))
        name_entry = QLineEdit(self.user_data['name'])
        delivery_layout.addWidget(name_entry)

        delivery_layout.addWidget(QLabel("Address:"))
        address_entry = QLineEdit(self.user_data['address'])
        delivery_layout.addWidget(address_entry)

        layout.addWidget(delivery_widget)

        # Buttons
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)

        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        cancel_button.clicked.connect(checkout_dialog.reject)

        confirm_button = QPushButton("Confirm Order")
        confirm_button.clicked.connect(
            lambda: self.place_order(
                name_entry.text(), address_entry.text(), checkout_dialog)
        )

        button_layout.addWidget(cancel_button)
        button_layout.addWidget(confirm_button)
        layout.addWidget(button_container)

        checkout_dialog.setStyleSheet(self.style_dict['common_styles'])
        checkout_dialog.exec()

    def place_order(self, name, address, checkout_dialog):
        if not name or not address:
            QMessageBox.critical(self, "Error", "Please fill in all fields.")
            return

        try:
            order = Order(self.cart[0][0].name, [item for _, item, _ in self.cart],
                          sum(details['price'] for _, _, details in self.cart), name, address)

            self.save_order(order)

            QMessageBox.information(
                self, "Order Placed", "Your order has been successfully placed!")
            self.cart.clear()
            self.update_cart_page()
            checkout_dialog.accept()
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"An error occurred while placing your order: {str(e)}")

    def save_order(self, order):
        conn = sqlite3.connect('orders.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS orders
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      restaurant TEXT,
                      items TEXT,
                      total REAL,
                      customer_name TEXT,
                      address TEXT,
                      timestamp TEXT)''')

        c.execute("INSERT INTO orders (restaurant, items, total, customer_name, address, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                  (order.restaurant, json.dumps(order.items), order.total, order.customer_name, order.address, order.timestamp.isoformat()))

        conn.commit()
        conn.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = QGuiApplication.primaryScreen().geometry()
    window = FoodOrderingApp()
    window.setGeometry(screen)
    window.show()
    sys.exit(app.exec())
