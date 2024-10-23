from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QMessageBox)
from PyQt6.QtCore import pyqtSignal
import sqlite3


class LoginDialog(QDialog):
    login_successful = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login / Sign Up")
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()

        self.email_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)

        button_layout = QHBoxLayout()
        self.login_button = QPushButton("Login")
        self.signup_button = QPushButton("Sign Up")
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.signup_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.login_button.clicked.connect(self.login)
        self.signup_button.clicked.connect(self.show_signup_dialog)

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
        signup_dialog = SignUpDialog()
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
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sign Up")
        self.setGeometry(200, 200, 300, 250)

        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.phone_input = QLineEdit()
        self.address_input = QLineEdit()

        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)
        layout.addWidget(QLabel("Phone:"))
        layout.addWidget(self.phone_input)
        layout.addWidget(QLabel("Address:"))
        layout.addWidget(self.address_input)

        self.signup_button = QPushButton("Sign Up")
        layout.addWidget(self.signup_button)

        self.setLayout(layout)

        self.signup_button.clicked.connect(self.signup)

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
