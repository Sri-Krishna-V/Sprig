'''
User (Base Class)
Purpose: Provides common functionalities for all users (e.g., login, registration).
Attributes:
user_id: Unique identifier for each user.
name: Name of the user.
email: Email of the user.
password: Hashed password for secure login.
Methods:
register(): Registers a new user.
login(): Authenticates a user based on email and password.
logout(): Ends the user's session.
Inheritance: Customer, RestaurantPartner, and DeliveryPartner inherit from this class.

'''

import sqlite3
from hashlib import sha256


DATABASE = 'sprig.db'


class User:
    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email

    def register(self):
        """
        Registers a new user.
        """
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Users (username, password)
                VALUES (?, ?)
            ''', (self.username, sha256(self.password.encode()).hexdigest()))
            conn.commit()
            conn.close()
            print(f"User {self.username} registered successfully.")
        except sqlite3.Error as e:
            print(f"Database error during user registration: {e}")

    @staticmethod
    def login(username, password):
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM Users WHERE username=? AND password=?
            ''', (username, password))
            user = cursor.fetchone()
            conn.close()
            if user:
                return User(user[1], user[2])
            else:
                return None
        except sqlite3.Error as e:
            print(f"Database error during login: {e}")
            return None

    def logout(self):
        """
        Ends the user's session.
        """
        print(f"User {self.username} logged out successfully.")
