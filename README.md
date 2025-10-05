# Food Delivery Management System

A comprehensive food delivery management system built with Python, Flask, SQLite, and modern web technologies. This application demonstrates various database operations, complex SQL queries, and professional frontend design.

## 📋 Features

### Database Features
- **Complete ER Diagram Implementation**: All entities from the provided ER diagram
- **10+ Complex SQL Queries**: Demonstrating joins, aggregations, subqueries, and filtering
- **Normalized Database Schema**: Proper relationships with foreign keys and constraints
- **Sample Data**: Realistic test data for demonstration

### Application Features
1. **Dashboard**: Overview of system statistics with real-time metrics
2. **Restaurant Management**: View restaurants with ratings, cuisine types, and details
3. **Order Management**: Track orders with filtering by status
4. **Analytics & Reports**: 
   - Restaurant revenue analysis
   - Delivery partner performance
   - Popular menu items
   - Payment method analysis
   - Cuisine-wise statistics
5. **Customer Insights**:
   - Top spending customers
   - Membership benefits tracking

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Install Required Packages

Open PowerShell in the project directory and run:

```powershell
pip install flask
```

### Step 2: Initialize Database

Run the database population script:

```powershell
python populate_data.py
```

This will:
- Create the SQLite database (`food_delivery.db`)
- Set up all tables with proper schema
- Insert sample data

### Step 3: Run the Application

Start the Flask server:

```powershell
python app.py
```

The application will be available at: **http://localhost:5000**

## 📊 Database Schema

### Tables Created:
1. **Users** - Authentication and user management
2. **Customers** - Customer details and contact information
3. **Restaurant** - Restaurant information with ratings
4. **RestaurantOwners** - Restaurant ownership details
5. **DeliveryPartners** - Delivery personnel information
6. **MenuItems** - Menu items for each restaurant
7. **Orders** - Order tracking and management
8. **OrderItems** - Individual items in each order
9. **Payments** - Payment tracking and methods
10. **Membership** - Customer membership programs
11. **Offers** - Promotional offers and discounts
12. **Carts** - Shopping cart management
13. **CartItems** - Items in customer carts

## 🔍 10 Key SQL Queries Implemented

### 1. **Restaurant Listing with Menu Count**
```sql
SELECT r.*, COUNT(DISTINCT m.menu_item_id) as menu_items_count
FROM Restaurant r
LEFT JOIN MenuItems m ON r.restaurant_id = m.restaurant_id
GROUP BY r.restaurant_id
ORDER BY r.rating DESC
```
**Purpose**: Get all restaurants with their ratings and number of menu items

### 2. **Top Customer Spending Analysis**
```sql
SELECT c.customer_id, c.customername, COUNT(DISTINCT o.order_id) as total_orders,
       SUM(o.total_amount) as total_spent, AVG(o.total_amount) as avg_order_value,
       m.membership_type
FROM Customers c
LEFT JOIN Orders o ON c.customer_id = o.customer_id
LEFT JOIN Membership m ON c.customer_id = m.customer_id
GROUP BY c.customer_id
HAVING total_orders > 0
ORDER BY total_spent DESC
```
**Purpose**: Identify top spending customers with their order patterns

### 3. **Menu Items with Restaurant Details**
```sql
SELECT m.*, r.restaurant_name, r.cuisine_type
FROM MenuItems m
JOIN Restaurant r ON m.restaurant_id = r.restaurant_id
WHERE m.availability = 1
ORDER BY m.price ASC
```
**Purpose**: Browse available menu items across restaurants

### 4. **Complete Order Details (Complex Join)**
```sql
SELECT o.*, c.customername, r.restaurant_name, d.name as delivery_partner,
       p.payment_method, p.payment_status
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id
JOIN Restaurant r ON o.restaurant_id = r.restaurant_id
LEFT JOIN DeliveryPartners d ON o.delivery_partner_id = d.d_id
LEFT JOIN Payments p ON o.order_id = p.order_id
ORDER BY o.order_date DESC
```
**Purpose**: Get comprehensive order information with all related entities

### 5. **Restaurant Revenue Analysis**
```sql
SELECT r.restaurant_id, r.restaurant_name, COUNT(DISTINCT o.order_id) as total_orders,
       SUM(o.total_amount) as total_revenue, AVG(o.total_amount) as avg_order_value,
       SUM(CASE WHEN o.order_status = 'delivered' THEN 1 ELSE 0 END) as delivered_orders,
       ROUND(SUM(CASE WHEN o.order_status = 'delivered' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as success_rate
FROM Restaurant r
LEFT JOIN Orders o ON r.restaurant_id = o.restaurant_id
GROUP BY r.restaurant_id
ORDER BY total_revenue DESC
```
**Purpose**: Analyze restaurant performance with success rates

### 6. **Delivery Partner Performance**
```sql
SELECT d.d_id, d.name, COUNT(o.order_id) as total_deliveries,
       SUM(CASE WHEN o.order_status = 'delivered' THEN 1 ELSE 0 END) as completed_deliveries,
       SUM(o.total_amount) as total_order_value
FROM DeliveryPartners d
LEFT JOIN Orders o ON d.d_id = o.delivery_partner_id
GROUP BY d.d_id
ORDER BY total_deliveries DESC
```
**Purpose**: Track delivery partner efficiency and workload

### 7. **Most Popular Menu Items**
```sql
SELECT m.menu_item_id, m.item_name, r.restaurant_name,
       COUNT(oi.order_item_id) as times_ordered,
       SUM(oi.item_quantity) as total_quantity_sold,
       SUM(oi.item_quantity * oi.item_price) as total_revenue
FROM MenuItems m
JOIN Restaurant r ON m.restaurant_id = r.restaurant_id
LEFT JOIN OrderItems oi ON m.menu_item_id = oi.menu_item_id
GROUP BY m.menu_item_id
HAVING times_ordered > 0
ORDER BY times_ordered DESC
```
**Purpose**: Identify bestselling menu items across all restaurants

### 8. **Membership Benefits Analysis (With Subquery)**
```sql
SELECT c.customer_id, c.customername, m.membership_type, m.discount_rate,
       (SELECT COUNT(*) FROM Orders o WHERE o.customer_id = c.customer_id) as total_orders,
       (SELECT SUM(o2.membership_discount) FROM Orders o2 WHERE o2.customer_id = c.customer_id) as total_savings
FROM Customers c
JOIN Membership m ON c.customer_id = m.customer_id
WHERE date(m.expiry_date) >= date('now')
ORDER BY m.discount_rate DESC
```
**Purpose**: Track active memberships and customer savings

### 9. **Payment Method Analysis**
```sql
SELECT p.payment_method, COUNT(p.payment_id) as transaction_count,
       SUM(p.amount) as total_amount, AVG(p.amount) as avg_transaction,
       SUM(CASE WHEN p.payment_status = 'completed' THEN 1 ELSE 0 END) as successful_transactions
FROM Payments p
GROUP BY p.payment_method
ORDER BY total_amount DESC
```
**Purpose**: Analyze payment preferences and success rates

### 10. **Cuisine-wise Statistics**
```sql
SELECT r.cuisine_type, COUNT(DISTINCT r.restaurant_id) as restaurant_count,
       COUNT(DISTINCT o.order_id) as total_orders,
       SUM(o.total_amount) as total_revenue,
       AVG(r.rating) as avg_rating
FROM Restaurant r
LEFT JOIN Orders o ON r.restaurant_id = o.restaurant_id
GROUP BY r.cuisine_type
ORDER BY total_revenue DESC
```
**Purpose**: Compare performance across different cuisine types

## 🎨 Frontend Features

- **Modern, Professional Design**: Gradient colors and smooth animations
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Interactive Navigation**: Tab-based interface for different sections
- **Real-time Data Visualization**: Dynamic tables and cards
- **Status Badges**: Color-coded order and payment status
- **Font Awesome Icons**: Professional iconography throughout

## 📁 Project Structure

```
Sprig/
│
├── app.py                      # Flask application with API routes
├── database_schema.sql         # Database schema definition
├── populate_data.py           # Sample data insertion script
├── food_delivery.db           # SQLite database (created after setup)
│
├── templates/
│   └── index.html             # Main HTML template
│
├── static/
│   ├── style.css              # CSS styles
│   └── script.js              # JavaScript for frontend
│
└── README.md                  # This file
```

## 🔧 API Endpoints

### Data Retrieval Endpoints
- `GET /api/restaurants` - List all restaurants
- `GET /api/customers/top-spenders` - Top spending customers
- `GET /api/menu` - Menu items (with filters)
- `GET /api/orders` - All orders (with status filter)
- `GET /api/analytics/restaurant-revenue` - Revenue analysis
- `GET /api/analytics/delivery-performance` - Delivery partner stats
- `GET /api/analytics/popular-items` - Popular menu items
- `GET /api/analytics/payment-methods` - Payment analysis
- `GET /api/analytics/cuisine-stats` - Cuisine statistics
- `GET /api/customers/membership` - Membership details
- `GET /api/dashboard/summary` - Dashboard statistics
- `GET /api/orders/<order_id>/items` - Order items details

### CRUD Operations
- `POST /api/orders/create` - Create new order
- `PUT /api/orders/<order_id>/status` - Update order status

## 💡 Key Technologies

- **Backend**: Python 3, Flask
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3 (with CSS Grid & Flexbox), Vanilla JavaScript
- **Icons**: Font Awesome 6
- **Design**: Modern gradient-based UI with responsive layout

## 📈 Sample Data Included

- 8 Customers
- 6 Restaurants (Various cuisines: Italian, American, Japanese, Mexican, Indian)
- 25+ Menu Items
- 5 Delivery Partners
- 8+ Sample Orders
- 5 Membership Plans
- 4 Active Offers

## 🔐 Database Relationships

The application properly implements:
- **One-to-One**: Users ↔ Customers, Users ↔ DeliveryPartners
- **One-to-Many**: Restaurant → MenuItems, Orders → OrderItems
- **Many-to-One**: Orders → Customers, Orders → Restaurant
- **Many-to-Many**: Customers ↔ MenuItems (through Cart/Order)

## 🎯 Use Cases Demonstrated

1. **Customer Journey**: Browse restaurants → View menu → Place order → Track delivery
2. **Restaurant Analytics**: Track revenue, popular items, success rate
3. **Delivery Management**: Assign partners, track performance
4. **Membership Program**: Discount tracking, savings calculation
5. **Business Intelligence**: Revenue analysis, payment trends, cuisine popularity

## 🛠️ Troubleshooting

### Database Not Found Error
```powershell
python populate_data.py
```

### Port Already in Use
Change the port in `app.py`:
```python
app.run(debug=True, port=5001)  # Change 5000 to 5001
```

### Module Not Found Error
```powershell
pip install flask
```

## 📝 Notes

- The application uses SQLite, which is file-based and doesn't require a separate database server
- All queries are optimized with proper indexes on foreign keys
- The frontend uses modern CSS features (Grid, Flexbox, Gradients)
- CORS is not enabled - frontend must be served from the same origin

## 🎓 Educational Value

This project demonstrates:
- Database design from ER diagrams
- SQL query writing (joins, aggregations, subqueries)
- RESTful API design
- Frontend-backend integration
- Responsive web design
- Professional UI/UX principles

## 👨‍💻 Author

Created for DBMS coursework - Semester 5

## 📄 License

This project is created for educational purposes.
