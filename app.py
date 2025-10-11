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

# Home route


@app.route('/')
def index():
    return render_template('index.html')

# Query 1: Get all restaurants with their ratings and cuisine types


@app.route('/api/restaurants')
def get_restaurants():
    try:
        cuisine_type = request.args.get('cuisine_type')
        min_rating = request.args.get('min_rating')
        search = request.args.get('search')

        conn = get_db_connection()
        query = '''
            SELECT r.restaurant_id, r.restaurant_name, r.restaurant_address, 
                   r.cuisine_type, r.rating, r.owner_id,
                   'Owner #' || COALESCE(r.owner_id, 0) as owner_name,
                   COUNT(DISTINCT m.menu_item_id) as menu_items_count
            FROM Restaurant r
            LEFT JOIN MenuItems m ON r.restaurant_id = m.restaurant_id
            WHERE 1=1
        '''
        params = []

        if cuisine_type:
            query += ' AND r.cuisine_type = ?'
            params.append(cuisine_type)

        if min_rating:
            query += ' AND r.rating >= ?'
            params.append(float(min_rating))

        if search:
            query += ' AND r.restaurant_name LIKE ?'
            params.append(f'%{search}%')

        query += '''
            GROUP BY r.restaurant_id
            ORDER BY r.rating DESC
        '''

        restaurants = conn.execute(query, params).fetchall()
        conn.close()
        return jsonify([dict_from_row(r) for r in restaurants])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get unique cuisine types for filter


@app.route('/api/restaurants/cuisines')
def get_cuisines():
    try:
        conn = get_db_connection()
        cuisines = conn.execute('''
            SELECT DISTINCT cuisine_type 
            FROM Restaurant 
            WHERE cuisine_type IS NOT NULL 
            ORDER BY cuisine_type
        ''').fetchall()
        conn.close()
        return jsonify([row['cuisine_type'] for row in cuisines])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Query 2: Get top customers by total spending (with joins and aggregation)


@app.route('/api/customers/top-spenders')
def top_spenders():
    try:
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
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Query 3: Get menu items with restaurant details (filtered by availability)


@app.route('/api/menu')
def get_menu():
    try:
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
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Query 4: Get order details with customer, restaurant, and delivery info (complex join)


@app.route('/api/orders')
def get_orders():
    try:
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
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
    try:
        conn = get_db_connection()
        items = conn.execute('''
            SELECT oi.order_item_id, oi.item_quantity as quantity, oi.item_price as price,
                   m.item_name, m.description, m.item_type,
                   o.order_id, o.order_date, o.order_status, o.total_amount,
                   c.customername, r.restaurant_name,
                   d.name as delivery_partner,
                   COALESCE(mem.discount_rate, 0) as membership_discount_rate,
                   ROUND(o.total_amount * COALESCE(mem.discount_rate, 0) / 100, 2) as membership_discount
            FROM OrderItems oi
            JOIN MenuItems m ON oi.menu_item_id = m.menu_item_id
            JOIN Orders o ON oi.order_id = o.order_id
            JOIN Customers c ON o.customer_id = c.customer_id
            JOIN Restaurant r ON o.restaurant_id = r.restaurant_id
            LEFT JOIN DeliveryPartners d ON o.delivery_partner_id = d.d_id
            LEFT JOIN Membership mem ON c.customer_id = mem.customer_id
            WHERE oi.order_id = ?
        ''', (order_id,)).fetchall()
        conn.close()

        if not items:
            return jsonify({'error': 'Order not found or has no items'}), 404

        return jsonify([dict_from_row(r) for r in items])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Query 11: Get available offers


@app.route('/api/offers')
def get_offers():
    try:
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
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

# Customer Analytics - Demographics


@app.route('/api/analytics/customer-demographics')
def customer_demographics():
    try:
        conn = get_db_connection()
        demographics = conn.execute('''
            SELECT 
                COUNT(DISTINCT c.customer_id) as total_customers,
                COUNT(DISTINCT CASE WHEN m.membership_type IS NOT NULL THEN c.customer_id END) as membership_customers,
                AVG(CASE WHEN o.customer_id IS NOT NULL THEN order_count ELSE 0 END) as avg_orders_per_customer,
                SUM(CASE WHEN order_count = 0 THEN 1 ELSE 0 END) as inactive_customers,
                SUM(CASE WHEN order_count >= 5 THEN 1 ELSE 0 END) as frequent_customers
            FROM Customers c
            LEFT JOIN Membership m ON c.customer_id = m.customer_id AND date(m.expiry_date) >= date('now')
            LEFT JOIN (
                SELECT customer_id, COUNT(*) as order_count
                FROM Orders
                GROUP BY customer_id
            ) o ON c.customer_id = o.customer_id
        ''').fetchone()
        conn.close()
        return jsonify(dict_from_row(demographics))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Customer Order Frequency Distribution


@app.route('/api/analytics/customer-order-frequency')
def customer_order_frequency():
    try:
        conn = get_db_connection()
        frequency = conn.execute('''
            SELECT 
                CASE 
                    WHEN order_count = 0 THEN 'No Orders'
                    WHEN order_count = 1 THEN '1 Order'
                    WHEN order_count BETWEEN 2 AND 5 THEN '2-5 Orders'
                    WHEN order_count BETWEEN 6 AND 10 THEN '6-10 Orders'
                    ELSE '10+ Orders'
                END as frequency_range,
                COUNT(*) as customer_count
            FROM (
                SELECT c.customer_id, COUNT(o.order_id) as order_count
                FROM Customers c
                LEFT JOIN Orders o ON c.customer_id = o.customer_id
                GROUP BY c.customer_id
            )
            GROUP BY frequency_range
            ORDER BY 
                CASE frequency_range
                    WHEN 'No Orders' THEN 1
                    WHEN '1 Order' THEN 2
                    WHEN '2-5 Orders' THEN 3
                    WHEN '6-10 Orders' THEN 4
                    ELSE 5
                END
        ''').fetchall()
        conn.close()
        return jsonify([dict_from_row(r) for r in frequency])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Customer Spending Distribution


@app.route('/api/analytics/customer-spending')
def customer_spending():
    try:
        conn = get_db_connection()
        spending = conn.execute('''
            SELECT 
                CASE 
                    WHEN total_spent IS NULL OR total_spent = 0 THEN '₹0'
                    WHEN total_spent < 500 THEN '₹1-499'
                    WHEN total_spent < 1000 THEN '₹500-999'
                    WHEN total_spent < 2000 THEN '₹1000-1999'
                    WHEN total_spent < 5000 THEN '₹2000-4999'
                    ELSE '₹5000+'
                END as spending_range,
                COUNT(*) as customer_count
            FROM (
                SELECT c.customer_id, SUM(o.total_amount) as total_spent
                FROM Customers c
                LEFT JOIN Orders o ON c.customer_id = o.customer_id
                GROUP BY c.customer_id
            )
            GROUP BY spending_range
            ORDER BY 
                CASE spending_range
                    WHEN '₹0' THEN 1
                    WHEN '₹1-499' THEN 2
                    WHEN '₹500-999' THEN 3
                    WHEN '₹1000-1999' THEN 4
                    WHEN '₹2000-4999' THEN 5
                    ELSE 6
                END
        ''').fetchall()
        conn.close()
        return jsonify([dict_from_row(r) for r in spending])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Customer Growth Trend


@app.route('/api/analytics/customer-growth')
def customer_growth():
    try:
        conn = get_db_connection()
        # Get customers with their first order date
        growth = conn.execute('''
            SELECT 
                strftime('%Y-%m', MIN(o.order_date)) as month,
                COUNT(DISTINCT o.customer_id) as new_customers
            FROM Orders o
            WHERE o.order_date IS NOT NULL
            GROUP BY strftime('%Y-%m', o.order_date)
            ORDER BY month DESC
            LIMIT 12
        ''').fetchall()
        conn.close()
        return jsonify([dict_from_row(r) for r in growth])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Menu Filters - Get price ranges


@app.route('/api/menu/price-ranges')
def menu_price_ranges():
    try:
        conn = get_db_connection()
        ranges = conn.execute('''
            SELECT 
                CASE 
                    WHEN price < 100 THEN 'Under ₹100'
                    WHEN price < 200 THEN '₹100-199'
                    WHEN price < 300 THEN '₹200-299'
                    WHEN price < 500 THEN '₹300-499'
                    ELSE '₹500+'
                END as price_range,
                COUNT(*) as item_count
            FROM MenuItems
            WHERE availability = 1
            GROUP BY price_range
            ORDER BY 
                CASE price_range
                    WHEN 'Under ₹100' THEN 1
                    WHEN '₹100-199' THEN 2
                    WHEN '₹200-299' THEN 3
                    WHEN '₹300-499' THEN 4
                    ELSE 5
                END
        ''').fetchall()
        conn.close()
        return jsonify([dict_from_row(r) for r in ranges])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Enhanced Menu API with more filters


@app.route('/api/menu/enhanced')
def get_enhanced_menu():
    try:
        restaurant_id = request.args.get('restaurant_id')
        item_type = request.args.get('item_type')
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')
        cuisine = request.args.get('cuisine')
        # price, popularity, name
        sort_by = request.args.get('sort_by', 'price')

        conn = get_db_connection()
        query = '''
            SELECT m.menu_item_id, m.item_name, m.description, m.price, 
                   m.item_type, m.availability, r.restaurant_name, r.cuisine_type,
                   r.restaurant_id,
                   COUNT(DISTINCT oi.order_item_id) as times_ordered
            FROM MenuItems m
            JOIN Restaurant r ON m.restaurant_id = r.restaurant_id
            LEFT JOIN OrderItems oi ON m.menu_item_id = oi.menu_item_id
            WHERE m.availability = 1
        '''
        params = []

        if restaurant_id:
            query += ' AND m.restaurant_id = ?'
            params.append(restaurant_id)

        if item_type:
            query += ' AND m.item_type = ?'
            params.append(item_type)

        if min_price:
            query += ' AND m.price >= ?'
            params.append(float(min_price))

        if max_price:
            query += ' AND m.price <= ?'
            params.append(float(max_price))

        if cuisine:
            query += ' AND r.cuisine_type = ?'
            params.append(cuisine)

        query += ' GROUP BY m.menu_item_id'

        # Add sorting
        if sort_by == 'popularity':
            query += ' ORDER BY times_ordered DESC, m.price ASC'
        elif sort_by == 'price_high':
            query += ' ORDER BY m.price DESC'
        elif sort_by == 'name':
            query += ' ORDER BY m.item_name ASC'
        else:  # default price low to high
            query += ' ORDER BY m.price ASC'

        items = conn.execute(query, params).fetchall()
        conn.close()
        return jsonify([dict_from_row(r) for r in items])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Offers with categories


@app.route('/api/offers/enhanced')
def get_enhanced_offers():
    try:
        status = request.args.get('status', 'active')  # active, expired, all
        min_discount = request.args.get('min_discount')
        offer_type = request.args.get('type')  # percentage, freebie, combo

        conn = get_db_connection()
        query = '''
            SELECT offer_id, offer_code, description, discount_percentage,
                   valid_from, valid_to, min_order_amount,
                   CASE 
                       WHEN discount_percentage >= 50 THEN 'Super Saver'
                       WHEN discount_percentage >= 30 THEN 'Great Deal'
                       WHEN discount_percentage >= 20 THEN 'Good Offer'
                       WHEN discount_percentage = 0 THEN 'Free Delivery'
                       ELSE 'Standard Offer'
                   END as offer_category,
                   CASE 
                       WHEN date(valid_to) >= date('now') THEN 'Active'
                       ELSE 'Expired'
                   END as status
            FROM Offers
            WHERE 1=1
        '''
        params = []

        if status == 'active':
            query += ' AND date(valid_to) >= date("now")'
        elif status == 'expired':
            query += ' AND date(valid_to) < date("now")'

        if min_discount:
            query += ' AND discount_percentage >= ?'
            params.append(float(min_discount))

        query += ' ORDER BY discount_percentage DESC, valid_to DESC'

        offers = conn.execute(query, params).fetchall()
        conn.close()
        return jsonify([dict_from_row(r) for r in offers])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
    try:
        data = request.json

        # Validate required fields
        if not data.get('customer_id') or not data.get('restaurant_id'):
            return jsonify({'success': False, 'error': 'Customer and restaurant are required'}), 400

        if not data.get('items') or len(data.get('items', [])) == 0:
            return jsonify({'success': False, 'error': 'At least one item is required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Calculate total amount from items
        total_amount = sum(item['price'] * item['quantity']
                           for item in data.get('items', []))

        # Apply offer discount if provided
        if data.get('offer_id'):
            offer = conn.execute('SELECT discount_percentage FROM Offers WHERE offer_id = ?',
                                 (data['offer_id'],)).fetchone()
            if offer:
                discount = (total_amount * offer['discount_percentage']) / 100
                total_amount -= discount

        # Insert order
        cursor.execute('''
            INSERT INTO Orders (customer_id, restaurant_id, delivery_partner_id, 
                               order_status, total_amount)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['customer_id'], data['restaurant_id'], data.get('delivery_partner_id'),
              'pending', total_amount))

        order_id = cursor.lastrowid

        # Insert order items
        for item in data.get('items', []):
            cursor.execute('''
                INSERT INTO OrderItems (order_id, menu_item_id, item_quantity, item_price)
                VALUES (?, ?, ?, ?)
            ''', (order_id, item['menu_item_id'], item['quantity'], item['price']))

        # Insert payment record
        if data.get('payment_method'):
            cursor.execute('''
                INSERT INTO Payments (order_id, payment_method, payment_status, amount)
                VALUES (?, ?, ?, ?)
            ''', (order_id, data['payment_method'], 'pending', total_amount))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'order_id': order_id, 'total_amount': total_amount})

    except KeyError as e:
        return jsonify({'success': False, 'error': f'Missing required field: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Update order status


@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    try:
        data = request.json

        if not data.get('status'):
            return jsonify({'success': False, 'error': 'Status is required'}), 400

        valid_statuses = ['pending', 'confirmed', 'preparing',
                          'out_for_delivery', 'delivered', 'cancelled']
        if data['status'] not in valid_statuses:
            return jsonify({'success': False, 'error': 'Invalid status'}), 400

        conn = get_db_connection()

        # Check if order exists
        order = conn.execute(
            'SELECT order_id FROM Orders WHERE order_id = ?', (order_id,)).fetchone()
        if not order:
            conn.close()
            return jsonify({'success': False, 'error': 'Order not found'}), 404

        conn.execute('''
            UPDATE Orders SET order_status = ? WHERE order_id = ?
        ''', (data['status'], order_id))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'order_id': order_id, 'new_status': data['status']})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
