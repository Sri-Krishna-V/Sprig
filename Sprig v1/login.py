from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QMessageBox, QWidget)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QScreen
import sqlite3


class LoginDialog(QDialog):
    login_successful = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login / Sign Up")
        self.setWindowFlags(Qt.WindowType.Window |
                            Qt.WindowType.FramelessWindowHint)
        self.showFullScreen()

        # Set the background gradient
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #E8F5E9, stop: 1 #F1F8E9
                );
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        content_widget = QWidget()
        content_widget.setFixedWidth(400)
        content_widget.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 20px;
                padding: 40px;
            }
        """)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)

        # Logo
        logo_label = QLabel("🍽️ SPRIG")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("""
            font-size: 48px;
            font-weight: bold;
            color: #2ECC71;
            margin-bottom: 20px;
            font-family: 'Arial Black';
        """)
        content_layout.addWidget(logo_label)

        # Input fields
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        content_layout.addWidget(self.email_input)
        content_layout.addWidget(self.password_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.login_button = QPushButton("Login")
        self.signup_button = QPushButton("Sign Up")
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.signup_button)

        content_layout.addLayout(button_layout)

        main_layout.addWidget(
            content_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        self.login_button.clicked.connect(self.login)
        self.signup_button.clicked.connect(self.show_signup_dialog)

        # Apply common styles
        self.setStyleSheet(self.setStyleSheet() + """
            QLineEdit {
                padding: 10px;
                border: 1px solid #BDC3C7;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton {
                background-color: #2ECC71;
                color: white;
                border: none;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #27AE60;
            }
        """)

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if self.check_credentials(email, password):
            user_data = self.get_user_data(email)
            self.login_successful.emit(user_data)
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed",
                                "Invalid email or password")

    def show_signup_dialog(self):
        signup_dialog = SignUpDialog(self)
        if signup_dialog.exec():
            QMessageBox.information(
                self, "Sign Up Successful", "You can now log in with your new account")

    def check_credentials(self, email, password):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()
        conn.close()
        return user is not None

    def get_user_data(self, email):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        conn.close()
        if user:
            return {
                "name": user[1],
                "email": user[2],
                "phone": user[4],
                "address": user[5]
            }
        return None


class SignUpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sign Up")
        self.setWindowFlags(Qt.WindowType.Window |
                            Qt.WindowType.FramelessWindowHint)
        self.showFullScreen()

        # Set the background gradient
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #E8F5E9, stop: 1 #F1F8E9
                );
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        content_widget = QWidget()
        content_widget.setFixedWidth(400)
        content_widget.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 20px;
                padding: 40px;
            }
        """)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)

        # Logo
        logo_label = QLabel("🍽️ SPRIG")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("""
            font-size: 48px;
            font-weight: bold;
            color: #2ECC71;
            margin-bottom: 20px;
            font-family: 'Arial Black';
        """)
        content_layout.addWidget(logo_label)

        # Input fields
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone")
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Address")

        content_layout.addWidget(self.name_input)
        content_layout.addWidget(self.email_input)
        content_layout.addWidget(self.password_input)
        content_layout.addWidget(self.phone_input)
        content_layout.addWidget(self.address_input)

        self.signup_button = QPushButton("Sign Up")
        content_layout.addWidget(self.signup_button)

        main_layout.addWidget(
            content_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        self.signup_button.clicked.connect(self.signup)

        # Apply common styles
        self.setStyleSheet(self.setStyleSheet() + """
            QLineEdit {
                padding: 10px;
                border: 1px solid #BDC3C7;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton {
                background-color: #2ECC71;
                color: white;
                border: none;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #27AE60;
            }
        """)

    def signup(self):
        name = self.name_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        phone = self.phone_input.text()
        address = self.address_input.text()

        if not all([name, email, password, phone, address]):
            QMessageBox.warning(self, "Sign Up Failed",
                                "Please fill in all fields")
            return

        if self.create_user(name, email, password, phone, address):
            self.accept()
        else:
            QMessageBox.warning(self, "Sign Up Failed", "Email already exists")

    def create_user(self, name, email, password, phone, address):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''CREATE TABLE IF NOT EXISTS users
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             name TEXT,
                             email TEXT UNIQUE,
                             password TEXT,
                             phone TEXT,
                             address TEXT)''')
            cursor.execute("INSERT INTO users (name, email, password, phone, address) VALUES (?, ?, ?, ?, ?)",
                           (name, email, password, phone, address))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
