# SQL Queries Documentation

This document explains all the SQL queries implemented in the Food Delivery Management System.

## Query Categories

### 1. Basic Retrieval Queries

### 2. Aggregation Queries

### 3. Join Queries

### 4. Subquery Queries

### 5. Analytical Queries

---

## Query 1: Restaurant Listing with Menu Count

**Category**: Join + Aggregation  
**API Endpoint**: `/api/restaurants`  
**Complexity**: Medium

```sql
SELECT r.restaurant_id, r.restaurant_name, r.restaurant_address, 
       r.cuisine_type, r.rating, ro.restaurant_name as owner_name,
       COUNT(DISTINCT m.menu_item_id) as menu_items_count
FROM Restaurant r
LEFT JOIN RestaurantOwners ro ON r.owner_id = ro.ro_id
LEFT JOIN MenuItems m ON r.restaurant_id = m.restaurant_id
GROUP BY r.restaurant_id
ORDER BY r.rating DESC
```

**Purpose**: Lists all restaurants with their ratings, addresses, and total number of menu items.

**Key Concepts**:

- LEFT JOIN to include restaurants even without menu items
- COUNT with DISTINCT to avoid duplicate counting
- GROUP BY for aggregation
- ORDER BY for sorting results

**Output**: Restaurant cards showing name, cuisine, rating, address, and menu count.

---

## Query 2: Top Customer Spending Analysis

**Category**: Multiple Joins + Aggregation + Filtering  
**API Endpoint**: `/api/customers/top-spenders`  
**Complexity**: High

```sql
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
```

**Purpose**: Identifies the top 10 customers by total spending with their order statistics.

**Key Concepts**:

- Multiple LEFT JOINs for related data
- Aggregate functions: COUNT, SUM, AVG
- HAVING clause to filter aggregated results
- LIMIT for top N results

**Business Value**: Customer segmentation, VIP identification, targeted marketing.

---

## Query 3: Available Menu Items with Restaurant Details

**Category**: Join + Filtering  
**API Endpoint**: `/api/menu`  
**Complexity**: Low

```sql
SELECT m.menu_item_id, m.item_name, m.description, m.price, 
       m.item_type, m.availability, r.restaurant_name, r.cuisine_type
FROM MenuItems m
JOIN Restaurant r ON m.restaurant_id = r.restaurant_id
WHERE m.availability = 1
  AND m.restaurant_id = ? (optional)
  AND m.item_type = ? (optional)
ORDER BY m.price ASC
```

**Purpose**: Browse menu items that are currently available for ordering.

**Key Concepts**:

- INNER JOIN (ensures only items with valid restaurants)
- WHERE clause with multiple conditions
- Dynamic filtering with parameters
- Sorting by price

**Use Case**: Customer menu browsing, filtering by restaurant or item type (veg/non-veg).

---

## Query 4: Complete Order Details (Complex Join)

**Category**: Multiple Joins (4+ tables)  
**API Endpoint**: `/api/orders`  
**Complexity**: High

```sql
SELECT o.order_id, o.order_date, o.order_status, o.total_amount,
       o.membership_discount,
       c.customername, c.email as customer_email,
       r.restaurant_name, r.cuisine_type,
       d.name as delivery_partner, d.phone_number as delivery_phone,
       p.payment_method, p.payment_status
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id
JOIN Restaurant r ON o.restaurant_id = r.restaurant_id
LEFT JOIN DeliveryPartners d ON o.delivery_partner_id = d.d_id
LEFT JOIN Payments p ON o.order_id = p.order_id
WHERE o.order_status = ? (optional)
ORDER BY o.order_date DESC
```

**Purpose**: Comprehensive order tracking with all related information.

**Key Concepts**:

- Multiple INNER and LEFT JOINs
- Joining 5 different tables
- Optional filtering by status
- Aliasing columns for clarity

**Business Value**: Order management, customer service, delivery tracking.

---

## Query 5: Restaurant Revenue Analysis

**Category**: Aggregation + Conditional Aggregation  
**API Endpoint**: `/api/analytics/restaurant-revenue`  
**Complexity**: High

```sql
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
```

**Purpose**: Analyze restaurant performance with revenue and success metrics.

**Key Concepts**:

- CASE statements for conditional aggregation
- Calculating percentages in SQL
- ROUND function for decimal precision
- Multiple aggregate functions

**Business Value**: Performance tracking, partner evaluation, business insights.

---

## Query 6: Delivery Partner Performance

**Category**: Aggregation + Conditional Counting  
**API Endpoint**: `/api/analytics/delivery-performance`  
**Complexity**: Medium

```sql
SELECT d.d_id, d.name, d.vehicle_type,
       COUNT(o.order_id) as total_deliveries,
       SUM(CASE WHEN o.order_status = 'delivered' THEN 1 ELSE 0 END) as completed_deliveries,
       SUM(o.total_amount) as total_order_value,
       ROUND(AVG(o.total_amount), 2) as avg_order_value
FROM DeliveryPartners d
LEFT JOIN Orders o ON d.d_id = o.delivery_partner_id
GROUP BY d.d_id
ORDER BY total_deliveries DESC
```

**Purpose**: Track delivery partner workload and performance.

**Key Concepts**:

- Aggregate functions on joined data
- CASE for conditional counting
- Performance metrics calculation

**Business Value**: Resource allocation, partner incentives, efficiency tracking.

---

## Query 7: Most Popular Menu Items

**Category**: Multiple Joins + Aggregation + Calculation  
**API Endpoint**: `/api/analytics/popular-items`  
**Complexity**: High

```sql
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
```

**Purpose**: Identify bestselling items across all restaurants.

**Key Concepts**:

- Joining through order items for sales data
- Calculating revenue in SQL
- HAVING to filter items with sales
- Top N with LIMIT

**Business Value**: Inventory planning, popular item promotion, menu optimization.

---

## Query 8: Membership Benefits Analysis (Subquery)

**Category**: Subqueries + Join  
**API Endpoint**: `/api/customers/membership`  
**Complexity**: High

```sql
SELECT c.customer_id, c.customername, c.email,
       m.membership_type, m.discount_rate, m.expiry_date,
       (SELECT COUNT(*) FROM Orders o WHERE o.customer_id = c.customer_id) as total_orders,
       (SELECT SUM(o2.membership_discount) FROM Orders o2 WHERE o2.customer_id = c.customer_id) as total_savings
FROM Customers c
JOIN Membership m ON c.customer_id = m.customer_id
WHERE date(m.expiry_date) >= date('now')
ORDER BY m.discount_rate DESC, total_orders DESC
```

**Purpose**: Track active memberships with customer savings.

**Key Concepts**:

- Correlated subqueries in SELECT clause
- Date comparison functions
- Multiple sorting criteria
- Calculating customer value

**Business Value**: Membership program analysis, retention strategies, customer rewards.

---

## Query 9: Payment Method Analysis

**Category**: Aggregation + Conditional Aggregation  
**API Endpoint**: `/api/analytics/payment-methods`  
**Complexity**: Medium

```sql
SELECT p.payment_method,
       COUNT(p.payment_id) as transaction_count,
       SUM(p.amount) as total_amount,
       AVG(p.amount) as avg_transaction,
       SUM(CASE WHEN p.payment_status = 'completed' THEN 1 ELSE 0 END) as successful_transactions,
       SUM(CASE WHEN p.payment_status = 'failed' THEN 1 ELSE 0 END) as failed_transactions
FROM Payments p
GROUP BY p.payment_method
ORDER BY total_amount DESC
```

**Purpose**: Analyze payment method preferences and success rates.

**Key Concepts**:

- GROUP BY single column
- Multiple CASE statements
- Success rate calculation (in frontend)

**Business Value**: Payment gateway optimization, user experience improvement, fraud detection.

---

## Query 10: Cuisine-wise Statistics

**Category**: Multiple Aggregations + Join  
**API Endpoint**: `/api/analytics/cuisine-stats`  
**Complexity**: Medium

```sql
SELECT r.cuisine_type,
       COUNT(DISTINCT r.restaurant_id) as restaurant_count,
       COUNT(DISTINCT o.order_id) as total_orders,
       SUM(o.total_amount) as total_revenue,
       AVG(r.rating) as avg_rating
FROM Restaurant r
LEFT JOIN Orders o ON r.restaurant_id = o.restaurant_id
GROUP BY r.cuisine_type
ORDER BY total_revenue DESC
```

**Purpose**: Compare performance across different cuisine types.

**Key Concepts**:

- Grouping by categorical data
- Multiple DISTINCT counts
- Average rating calculation

**Business Value**: Market trends, expansion planning, restaurant recruitment strategy.

---

## Bonus Query 11: Order Items Details

**Category**: Join with Calculation  
**API Endpoint**: `/api/orders/<order_id>/items`  
**Complexity**: Low

```sql
SELECT oi.order_item_id, oi.item_quantity, oi.item_price,
       m.item_name, m.description, m.item_type,
       (oi.item_quantity * oi.item_price) as subtotal
FROM OrderItems oi
JOIN MenuItems m ON oi.menu_item_id = m.menu_item_id
WHERE oi.order_id = ?
```

**Purpose**: Get detailed breakdown of items in a specific order.

**Key Concepts**:

- Calculated columns in SELECT
- WHERE clause with parameter
- Simple JOIN

**Use Case**: Order detail view, invoice generation, customer queries.

---

## Bonus Query 12: Dashboard Summary

**Category**: Multiple Single-row Aggregations  
**API Endpoint**: `/api/dashboard/summary`  
**Complexity**: Low

```sql
-- Total Customers
SELECT COUNT(*) as count FROM Customers

-- Total Restaurants
SELECT COUNT(*) as count FROM Restaurant

-- Total Orders
SELECT COUNT(*) as count FROM Orders

-- Total Revenue (delivered only)
SELECT COALESCE(SUM(total_amount), 0) as revenue 
FROM Orders 
WHERE order_status = 'delivered'

-- Active Orders
SELECT COUNT(*) as count 
FROM Orders 
WHERE order_status IN ('pending', 'confirmed', 'preparing', 'out_for_delivery')
```

**Purpose**: Quick statistics for dashboard overview.

**Key Concepts**:

- Simple COUNT queries
- COALESCE for NULL handling
- IN clause for multiple values
- WHERE filtering

**Business Value**: Quick business health check, executive dashboard.

---

## Query Complexity Breakdown

### Simple Queries (1-2 tables)

- Query 3: Menu Items
- Query 11: Order Items
- Query 12: Dashboard Stats

### Medium Complexity (2-3 tables + aggregation)

- Query 1: Restaurant Listing
- Query 6: Delivery Performance
- Query 9: Payment Analysis
- Query 10: Cuisine Stats

### High Complexity (4+ tables, subqueries, complex aggregation)

- Query 2: Top Spenders
- Query 4: Complete Orders
- Query 5: Restaurant Revenue
- Query 7: Popular Items
- Query 8: Membership Analysis

---

## SQL Concepts Demonstrated

✅ **Joins**: INNER JOIN, LEFT JOIN, Multiple table joins  
✅ **Aggregation**: COUNT, SUM, AVG, GROUP BY, HAVING  
✅ **Subqueries**: Correlated subqueries in SELECT  
✅ **Conditional Logic**: CASE statements  
✅ **Calculations**: Mathematical operations in queries  
✅ **Filtering**: WHERE, HAVING, date comparisons  
✅ **Sorting**: ORDER BY with multiple columns  
✅ **Limiting**: LIMIT for top N results  
✅ **Null Handling**: COALESCE, LEFT JOIN  
✅ **Functions**: ROUND, DISTINCT, date functions

---

## Performance Considerations

All queries are optimized with:

- Indexes on foreign keys
- Proper JOIN types (LEFT vs INNER)
- DISTINCT only where necessary
- Limited result sets where appropriate

## Testing Recommendations

1. Test each query with and without filters
2. Verify results with small data sets first
3. Check NULL handling for optional relationships
4. Validate calculations manually for accuracy
5. Test with various order status values
6. Check date comparisons across time zones
