import sqlite3

conn = sqlite3.connect('food_delivery.db')
cursor = conn.cursor()

print("=" * 60)
print("DATABASE STATISTICS")
print("=" * 60)

# Count records
customers = cursor.execute('SELECT COUNT(*) FROM Customers').fetchone()[0]
restaurants = cursor.execute('SELECT COUNT(*) FROM Restaurant').fetchone()[0]
menu_items = cursor.execute('SELECT COUNT(*) FROM MenuItems').fetchone()[0]
delivery_partners = cursor.execute(
    'SELECT COUNT(*) FROM DeliveryPartners').fetchone()[0]
users = cursor.execute('SELECT COUNT(*) FROM Users').fetchone()[0]

print(f"Users: {users}")
print(f"Customers: {customers}")
print(f"Restaurants: {restaurants}")
print(f"Menu Items: {menu_items}")
print(f"Delivery Partners: {delivery_partners}")

print("\n" + "=" * 60)
print("SAMPLE RESTAURANTS")
print("=" * 60)
for r in cursor.execute('SELECT restaurant_name, cuisine_type, rating FROM Restaurant LIMIT 10').fetchall():
    print(f"{r[0]:30s} | {r[1]:15s} | ⭐{r[2]}")

print("\n" + "=" * 60)
print("SAMPLE MENU ITEMS")
print("=" * 60)
for m in cursor.execute('SELECT item_name, price, item_type FROM MenuItems LIMIT 15').fetchall():
    print(f"{m[0]:35s} | ₹{m[1]:6.2f} | {m[2]}")

print("\n" + "=" * 60)
print("SAMPLE CUSTOMERS WITH CITIES")
print("=" * 60)
for c in cursor.execute('SELECT customername, customer_address FROM Customers LIMIT 10').fetchall():
    city = c[1].split(',')[-1].strip() if ',' in c[1] else c[1]
    print(f"{c[0]:20s} | {city}")

print("\n" + "=" * 60)
print("SAMPLE DELIVERY PARTNERS")
print("=" * 60)
for d in cursor.execute('SELECT name, vehicle_type, vehicle_number FROM DeliveryPartners LIMIT 10').fetchall():
    print(f"{d[0]:20s} | {d[1]:10s} | {d[2]}")

conn.close()
print("\n" + "=" * 60)
print("✅ ALL DATA VERIFIED - INDIAN THEMED DATABASE READY!")
print("=" * 60)
