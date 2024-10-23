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
import bcrypt


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
            hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute('''
                INSERT INTO Users (username, password, name, email)
                VALUES (?, ?, ?, ?)
            ''', (self.username, hashed_password, self.name, self.email))
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
                SELECT id, username, password, name, email, user_type 
                FROM Users 
                WHERE username=?
            ''', (username,))
            user = cursor.fetchone()
            conn.close()
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
                return {
                    'id': user[0],
                    'username': user[1],
                    'name': user[3],
                    'email': user[4],
                    'user_type': user[5]
                }
            return None
        except sqlite3.Error as e:
            print(f"Database error during login: {e}")
            return None

    def logout(self):
        """
        Ends the user's session.
        """
        print(f"User {self.username} logged out successfully.")
