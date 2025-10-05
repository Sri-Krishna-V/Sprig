from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

DATABASE = 'food_delivery.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def dict_from_row(row):
    return dict(zip(row.keys(), row))

# Home route


@app.route('/')
def index():
    return render_template('index.html')

# Query 1: Get all restaurants with their ratings and cuisine types


@app.route('/api/restaurants')
def get_restaurants():
    conn = get_db_connection()
    restaurants = conn.execute('''
        SELECT r.restaurant_id, r.restaurant_name, r.restaurant_address, 
               r.cuisine_type, r.rating,
               COUNT(DISTINCT m.menu_item_id) as menu_items_count
        FROM Restaurant r
        LEFT JOIN MenuItems m ON r.restaurant_id = m.restaurant_id
        GROUP BY r.restaurant_id
        ORDER BY r.rating DESC
    ''').fetchall()
    conn.close()
    return jsonify([dict_from_row(r) for r in restaurants])

# Query 2: Get top customers by total spending (with joins and aggregation)


@app.route('/api/customers/top-spenders')
def top_spenders():
    conn = get_db_connection()
    customers = conn.execute('''
        SELECT c.customer_id, c.customername, c.email, 
               COUNT(DISTINCT o.order_id) as total_orders,
               SUM(o.total_amount) as total_spent,
               AVG(o.total_amount) as avg_order_value,
               m.membership_type
        FROM Customers c
        LEFT JOIN Orders o ON c.customer_id = o.customer_id
        LEFT JOIN Membership m ON c.customer_id = m.customer_id
        GROUP BY c.customer_id
        HAVING total_orders > 0
        ORDER BY total_spent DESC
        LIMIT 10
    ''').fetchall()
    conn.close()
    return jsonify([dict_from_row(r) for r in customers])

# Query 3: Get menu items with restaurant details (filtered by availability)


@app.route('/api/menu')
def get_menu():
    restaurant_id = request.args.get('restaurant_id')
    item_type = request.args.get('item_type')

    conn = get_db_connection()
    query = '''
        SELECT m.menu_item_id, m.item_name, m.description, m.price, 
               m.item_type, m.availability, r.restaurant_name, r.cuisine_type
        FROM MenuItems m
        JOIN Restaurant r ON m.restaurant_id = r.restaurant_id
        WHERE m.availability = 1
    '''
    params = []

    if restaurant_id:
        query += ' AND m.restaurant_id = ?'
        params.append(restaurant_id)

    if item_type:
        query += ' AND m.item_type = ?'
        params.append(item_type)

    query += ' ORDER BY m.price ASC'

    items = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict_from_row(r) for r in items])

# Query 4: Get order details with customer, restaurant, and delivery info (complex join)


@app.route('/api/orders')
def get_orders():
    status = request.args.get('status')
    customer_id = request.args.get('customer_id')

    conn = get_db_connection()
    query = '''
        SELECT o.order_id, o.order_date, o.order_status, o.total_amount,
               c.customername, c.email as customer_email,
               r.restaurant_name, r.cuisine_type,
               d.name as delivery_partner, d.phone_number as delivery_phone,
               p.payment_method, p.payment_status,
               COALESCE(m.discount_rate, 0) as membership_discount_rate,
               ROUND(o.total_amount * COALESCE(m.discount_rate, 0) / 100, 2) as membership_discount
        FROM Orders o
        JOIN Customers c ON o.customer_id = c.customer_id
        JOIN Restaurant r ON o.restaurant_id = r.restaurant_id
        LEFT JOIN DeliveryPartners d ON o.delivery_partner_id = d.d_id
        LEFT JOIN Payments p ON o.order_id = p.order_id
        LEFT JOIN Membership m ON c.customer_id = m.customer_id
        WHERE 1=1
    '''
    params = []

    if status:
        query += ' AND o.order_status = ?'
        params.append(status)

    if customer_id:
        query += ' AND o.customer_id = ?'
        params.append(customer_id)

    query += ' ORDER BY o.order_date DESC'

    orders = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict_from_row(r) for r in orders])

# Query 5: Get restaurant revenue analysis (aggregation with grouping)


@app.route('/api/analytics/restaurant-revenue')
def restaurant_revenue():
    conn = get_db_connection()
    revenue = conn.execute('''
        SELECT r.restaurant_id, r.restaurant_name, r.cuisine_type,
               COUNT(DISTINCT o.order_id) as total_orders,
               SUM(o.total_amount) as total_revenue,
               AVG(o.total_amount) as avg_order_value,
               SUM(CASE WHEN o.order_status = 'delivered' THEN 1 ELSE 0 END) as delivered_orders,
               ROUND(SUM(CASE WHEN o.order_status = 'delivered' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as success_rate
        FROM Restaurant r
        LEFT JOIN Orders o ON r.restaurant_id = o.restaurant_id
        GROUP BY r.restaurant_id
        ORDER BY total_revenue DESC
    ''').fetchall()
    conn.close()
    return jsonify([dict_from_row(r) for r in revenue])

# Query 6: Get delivery partner performance (aggregation)


@app.route('/api/analytics/delivery-performance')
def delivery_performance():
    conn = get_db_connection()
    performance = conn.execute('''
        SELECT d.d_id, d.name, d.vehicle_type,
               COUNT(o.order_id) as total_deliveries,
               SUM(CASE WHEN o.order_status = 'delivered' THEN 1 ELSE 0 END) as completed_deliveries,
               SUM(o.total_amount) as total_order_value,
               ROUND(AVG(o.total_amount), 2) as avg_order_value
        FROM DeliveryPartners d
        LEFT JOIN Orders o ON d.d_id = o.delivery_partner_id
        GROUP BY d.d_id
        ORDER BY total_deliveries DESC
    ''').fetchall()
    conn.close()
    return jsonify([dict_from_row(r) for r in performance])

# Query 7: Get popular menu items (most ordered)


@app.route('/api/analytics/popular-items')
def popular_items():
    conn = get_db_connection()
    items = conn.execute('''
        SELECT m.menu_item_id, m.item_name, m.price, m.item_type,
               r.restaurant_name,
               COUNT(oi.order_item_id) as times_ordered,
               SUM(oi.item_quantity) as total_quantity_sold,
               SUM(oi.item_quantity * oi.item_price) as total_revenue
        FROM MenuItems m
        JOIN Restaurant r ON m.restaurant_id = r.restaurant_id
        LEFT JOIN OrderItems oi ON m.menu_item_id = oi.menu_item_id
        GROUP BY m.menu_item_id
        HAVING times_ordered > 0
        ORDER BY times_ordered DESC
        LIMIT 15
    ''').fetchall()
    conn.close()
    return jsonify([dict_from_row(r) for r in items])

# Query 8: Get customers with membership benefits (subquery)


@app.route('/api/customers/membership')
def membership_customers():
    conn = get_db_connection()
    customers = conn.execute('''
        SELECT c.customer_id, c.customername, c.email,
               m.membership_type, m.discount_rate, m.expiry_date,
               (SELECT COUNT(*) FROM Orders o WHERE o.customer_id = c.customer_id) as total_orders,
               (SELECT ROUND(SUM(o2.total_amount * m.discount_rate / 100), 2) 
                FROM Orders o2 
                WHERE o2.customer_id = c.customer_id) as total_savings
        FROM Customers c
        JOIN Membership m ON c.customer_id = m.customer_id
        WHERE date(m.expiry_date) >= date('now')
        ORDER BY m.discount_rate DESC, total_orders DESC
    ''').fetchall()
    conn.close()
    return jsonify([dict_from_row(r) for r in customers])

# Query 9: Get payment method analysis


@app.route('/api/analytics/payment-methods')
def payment_analysis():
    conn = get_db_connection()
    payments = conn.execute('''
        SELECT p.payment_method,
               COUNT(p.payment_id) as transaction_count,
               SUM(p.amount) as total_amount,
               AVG(p.amount) as avg_transaction,
               SUM(CASE WHEN p.payment_status = 'completed' THEN 1 ELSE 0 END) as successful_transactions,
               SUM(CASE WHEN p.payment_status = 'failed' THEN 1 ELSE 0 END) as failed_transactions
        FROM Payments p
        GROUP BY p.payment_method
        ORDER BY total_amount DESC
    ''').fetchall()
    conn.close()
    return jsonify([dict_from_row(r) for r in payments])

# Query 10: Get order items details for specific order


@app.route('/api/orders/<int:order_id>/items')
def get_order_items(order_id):
    conn = get_db_connection()
    items = conn.execute('''
        SELECT oi.order_item_id, oi.item_quantity, oi.item_price,
               m.item_name, m.description, m.item_type,
               (oi.item_quantity * oi.item_price) as subtotal
        FROM OrderItems oi
        JOIN MenuItems m ON oi.menu_item_id = m.menu_item_id
        WHERE oi.order_id = ?
    ''', (order_id,)).fetchall()
    conn.close()
    return jsonify([dict_from_row(r) for r in items])

# Query 11: Get available offers


@app.route('/api/offers')
def get_offers():
    conn = get_db_connection()
    offers = conn.execute('''
        SELECT offer_id, offer_code, description, discount_percentage,
               valid_from, valid_to, min_order_amount
        FROM Offers
        WHERE date(valid_to) >= date('now')
        ORDER BY discount_percentage DESC
    ''').fetchall()
    conn.close()
    return jsonify([dict_from_row(r) for r in offers])

# Query 12: Get cuisine-wise statistics


@app.route('/api/analytics/cuisine-stats')
def cuisine_stats():
    conn = get_db_connection()
    stats = conn.execute('''
        SELECT r.cuisine_type,
               COUNT(DISTINCT r.restaurant_id) as restaurant_count,
               COUNT(DISTINCT o.order_id) as total_orders,
               SUM(o.total_amount) as total_revenue,
               AVG(r.rating) as avg_rating
        FROM Restaurant r
        LEFT JOIN Orders o ON r.restaurant_id = o.restaurant_id
        GROUP BY r.cuisine_type
        ORDER BY total_revenue DESC
    ''').fetchall()
    conn.close()
    return jsonify([dict_from_row(r) for r in stats])

# Additional route for dashboard summary


@app.route('/api/dashboard/summary')
def dashboard_summary():
    conn = get_db_connection()

    # Get various statistics
    total_customers = conn.execute(
        'SELECT COUNT(*) as count FROM Customers').fetchone()['count']
    total_restaurants = conn.execute(
        'SELECT COUNT(*) as count FROM Restaurant').fetchone()['count']
    total_orders = conn.execute(
        'SELECT COUNT(*) as count FROM Orders').fetchone()['count']
    total_revenue = conn.execute(
        'SELECT COALESCE(SUM(total_amount), 0) as revenue FROM Orders WHERE order_status = "delivered"').fetchone()['revenue']
    active_orders = conn.execute(
        'SELECT COUNT(*) as count FROM Orders WHERE order_status IN ("pending", "confirmed", "preparing", "out_for_delivery")').fetchone()['count']

    conn.close()

    return jsonify({
        'total_customers': total_customers,
        'total_restaurants': total_restaurants,
        'total_orders': total_orders,
        'total_revenue': float(total_revenue),
        'active_orders': active_orders
    })

# CRUD Operations for demonstration

# Create new order


@app.route('/api/orders/create', methods=['POST'])
def create_order():
    data = request.json
    conn = get_db_connection()

    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Orders (customer_id, restaurant_id, delivery_partner_id, 
                           order_status, total_amount)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['customer_id'], data['restaurant_id'], data.get('delivery_partner_id'),
          'pending', data['total_amount']))

    order_id = cursor.lastrowid

    # Insert order items
    for item in data.get('items', []):
        cursor.execute('''
            INSERT INTO OrderItems (order_id, menu_item_id, item_quantity, item_price)
            VALUES (?, ?, ?, ?)
        ''', (order_id, item['menu_item_id'], item['quantity'], item['price']))

    conn.commit()
    conn.close()

    return jsonify({'success': True, 'order_id': order_id})

# Update order status


@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    data = request.json
    conn = get_db_connection()

    conn.execute('''
        UPDATE Orders SET order_status = ? WHERE order_id = ?
    ''', (data['status'], order_id))

    conn.commit()
    conn.close()

    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
