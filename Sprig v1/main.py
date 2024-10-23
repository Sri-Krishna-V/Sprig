import tkinter as tk
from tkinter import ttk, messagebox
import json
import sqlite3
from datetime import datetime


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


class FoodOrderingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Food Ordering App")
        self.master.geometry("800x600")

        self.restaurants = self.load_restaurants()
        self.cart = []

        self.create_widgets()

    def load_restaurants(self):
        try:
            with open(r'C:\Users\srikr\Desktop\Studies\Sem 3\OOPs by Python\Project\Sprig\Sprig v1\restaurants.json', 'r') as f:
                data = json.load(f)
                return [Restaurant(r['name'], r['menu']) for r in data]
        except FileNotFoundError:
            messagebox.showerror("Error", "Restaurants data file not found.")
            return []
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid restaurants data file.")
            return []

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill="both")

        self.home_frame = ttk.Frame(self.notebook)
        self.restaurant_frame = ttk.Frame(self.notebook)
        self.cart_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.home_frame, text="Home")
        self.notebook.add(self.restaurant_frame, text="Restaurants")
        self.notebook.add(self.cart_frame, text="Cart")

        self.create_home_page()
        self.create_restaurant_page()
        self.create_cart_page()

    def create_home_page(self):
        ttk.Label(self.home_frame, text="Welcome to Food Ordering App",
                  font=("Arial", 16)).pack(pady=20)
        ttk.Button(self.home_frame, text="Browse Restaurants",
                   command=lambda: self.notebook.select(1)).pack()

    def create_restaurant_page(self):
        for restaurant in self.restaurants:
            frame = ttk.Frame(self.restaurant_frame)
            frame.pack(pady=10, padx=10, fill="x")
            ttk.Label(frame, text=restaurant.name,
                      font=("Arial", 14)).pack(side="left")
            ttk.Button(frame, text="View Menu", command=lambda r=restaurant: self.show_menu(
                r)).pack(side="right")

    def show_menu(self, restaurant):
        menu_window = tk.Toplevel(self.master)
        menu_window.title(f"{restaurant.name} Menu")
        menu_window.geometry("400x400")

        for item, details in restaurant.menu.items():
            frame = ttk.Frame(menu_window)
            frame.pack(pady=5, padx=10, fill="x")
            ttk.Label(frame, text=f"{
                      item} - Rs.{details['price']}", font=("Arial", 12)).pack(side="left")
            ttk.Button(frame, text="Add to Cart", command=lambda i=item,
                       d=details: self.add_to_cart(restaurant, i, d)).pack(side="right")

    def add_to_cart(self, restaurant, item, details):
        self.cart.append((restaurant, item, details))
        messagebox.showinfo("Added to Cart", f"{
                            item} has been added to your cart.")
        self.update_cart_page()

    def create_cart_page(self):
        self.cart_items_frame = ttk.Frame(self.cart_frame)
        self.cart_items_frame.pack(expand=True, fill="both")

        self.checkout_button = ttk.Button(
            self.cart_frame, text="Proceed to Checkout", command=self.checkout)
        self.checkout_button.pack(pady=10)

        self.update_cart_page()

    def update_cart_page(self):
        for widget in self.cart_items_frame.winfo_children():
            widget.destroy()

        if not self.cart:
            ttk.Label(self.cart_items_frame, text="Your cart is empty",
                      font=("Arial", 14)).pack(pady=20)
            self.checkout_button.config(state="disabled")
        else:
            self.checkout_button.config(state="normal")
            for restaurant, item, details in self.cart:
                frame = ttk.Frame(self.cart_items_frame)
                frame.pack(pady=5, padx=10, fill="x")
                ttk.Label(frame, text=f"{
                          item} - Rs.{details['price']}", font=("Arial", 12)).pack(side="left")
                ttk.Button(frame, text="Remove", command=lambda r=restaurant, i=item,
                           d=details: self.remove_from_cart(r, i, d)).pack(side="right")

    def remove_from_cart(self, restaurant, item, details):
        self.cart.remove((restaurant, item, details))
        self.update_cart_page()

    def checkout(self):
        checkout_window = tk.Toplevel(self.master)
        checkout_window.title("Checkout")
        checkout_window.geometry("400x300")

        ttk.Label(checkout_window, text="Order Summary",
                  font=("Arial", 16)).pack(pady=10)

        total = sum(details['price'] for _, _, details in self.cart)
        for restaurant, item, details in self.cart:
            ttk.Label(checkout_window, text=f"{
                      item} - Rs.{details['price']}").pack()

        ttk.Label(checkout_window, text=f"Total: Rs.{
                  total}", font=("Arial", 14)).pack(pady=10)

        ttk.Label(checkout_window, text="Name:").pack()
        name_entry = ttk.Entry(checkout_window)
        name_entry.pack()

        ttk.Label(checkout_window, text="Address:").pack()
        address_entry = ttk.Entry(checkout_window)
        address_entry.pack()

        ttk.Button(checkout_window, text="Place Order", command=lambda: self.place_order(
            name_entry.get(), address_entry.get(), checkout_window)).pack(pady=10)

    def place_order(self, name, address, checkout_window):
        if not name or not address:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            order = Order(self.cart[0][0].name, [item for _, item, _ in self.cart],
                          sum(details['price'] for _, _, details in self.cart), name, address)

            self.save_order(order)

            messagebox.showinfo(
                "Order Placed", "Your order has been successfully placed!")
            self.cart.clear()
            self.update_cart_page()
            checkout_window.destroy()
        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while placing your order: {str(e)}")

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
    root = tk.Tk()
    app = FoodOrderingApp(root)
    root.mainloop()
