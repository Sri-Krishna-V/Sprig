# SQL Queries Documentation

This document explains all the SQL queries implemented in the Food Delivery Management System with **Indian-themed data**.

## Database Overview

- **91 Users** (63 customers + 25 delivery partners + 3 system users)
- **58 Customers** across major Indian cities (Bangalore, Mumbai, Delhi, Hyderabad, Chennai, Kolkata, Pune, Kochi)
- **15 Restaurants** serving authentic Indian cuisines
- **75 Menu Items** featuring popular Indian dishes
- **25 Delivery Partners** with state-specific vehicle registrations

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

**Sample Output** (Indian restaurants):

```
Restaurant: Biryani House
Cuisine: Indian | Rating: ⭐4.5
Address: 100 MG Road, Bangalore
Menu Items: 5 dishes

Restaurant: South Indian Express
Cuisine: South Indian | Rating: ⭐4.6
Address: 200 Anna Salai, Chennai
Menu Items: 5 dishes

Restaurant: Punjabi Dhaba
Cuisine: North Indian | Rating: ⭐4.4
Address: 300 Connaught Place, Delhi
Menu Items: 5 dishes
```

**Use Case**: Browse restaurants offering Biryani, Dosas, North Indian, South Indian, Seafood, etc.

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

**Sample Output** (Indian customers):

```
Top Customer: Rahul Sharma (rahul.sharma@email.com)
Total Orders: 15 | Total Spent: ₹8,450 | Avg Order: ₹563
Membership: Gold (10% discount)

Customer: Priya Patel (priya.patel@email.com)
Total Orders: 12 | Total Spent: ₹6,890 | Avg Order: ₹574
Membership: Silver (5% discount)
```

**Business Value**:

- Identify VIP customers across Bangalore, Mumbai, Delhi, Hyderabad
- Target high-value customers for premium membership upgrades
- Personalized marketing for top spenders
- Customer loyalty programs

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

**Sample Menu Items** (Indian dishes):

```
Masala Dosa - ₹89 (veg) - South Indian Express
Hyderabadi Chicken Biryani - ₹299 (non-veg) - Biryani House
Butter Chicken - ₹349 (non-veg) - Punjabi Dhaba
Pani Puri - ₹59 (veg) - Chat Corner
Filter Coffee - ₹39 (veg) - South Indian Express
```

**Use Case**:

- Browse vegetarian/non-vegetarian options
- Filter by restaurant (e.g., "Show me all items from Biryani House")
- Search by cuisine (North Indian, South Indian, Street Food, etc.)
- Sort by price (budget-friendly options)

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

**Sample Output** (Indian context):

```
Order #1245
Date: 2025-10-05 14:30:00 | Status: Out for Delivery | Total: ₹549

Customer: Rahul Sharma (rahul.sharma@email.com)
Restaurant: Biryani House (Indian cuisine)
Delivery Partner: Rajesh Kumar (9998887770)
Payment: UPI - Completed
Items: Hyderabadi Chicken Biryani, Raita, Gulab Jamun
```

**Business Value**:

- Real-time order tracking for customers
- Delivery partner assignment and coordination
- Customer service support
- Order history and analytics
- Payment reconciliation

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

**Sample Analytics** (Indian restaurants):

```
Restaurant: Hyderabadi Biryani Corner
Cuisine: Hyderabadi | Orders: 45 | Revenue: ₹14,805
Avg Order: ₹329 | Delivered: 42 | Success Rate: 93.33%

Restaurant: Punjabi Dhaba
Cuisine: North Indian | Orders: 38 | Revenue: ₹12,462
Avg Order: ₹328 | Delivered: 36 | Success Rate: 94.74%

Restaurant: Chat Corner
Cuisine: Street Food | Orders: 52 | Revenue: ₹4,680
Avg Order: ₹90 | Delivered: 50 | Success Rate: 96.15%
```

**Business Value**:

- Identify top-performing restaurants in each city
- Compare success rates across cuisine types
- Revenue tracking for commission calculations
- Partner performance evaluation
- Expansion decisions (which cuisines to add more)

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

**Sample Output** (Indian delivery partners):

```
Partner: Rajesh Kumar
Vehicle: Bike (KA01AB1234)
Total Deliveries: 47 | Completed: 45 | Order Value: ₹15,630
Avg Order: ₹332.55

Partner: Suresh Singh
Vehicle: Scooter (MH02CD5678)
Total Deliveries: 38 | Completed: 37 | Order Value: ₹11,286
Avg Order: ₹297.00

Partner: Manoj Sharma
Vehicle: Bike (DL03EF9012)
Total Deliveries: 42 | Completed: 40 | Order Value: ₹13,440
Avg Order: ₹320.00
```

**Business Value**:

- Resource allocation across Bangalore, Mumbai, Delhi zones
- Performance-based incentives
- Identify reliable delivery partners
- Workload balancing
- Vehicle type effectiveness analysis (Bike vs Scooter)

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

**Top Indian Dishes**:

```
1. Hyderabadi Chicken Biryani (Biryani House)
   Ordered: 156 times | Qty Sold: 189 | Revenue: ₹56,511

2. Masala Dosa (South Indian Express)
   Ordered: 142 times | Qty Sold: 178 | Revenue: ₹15,842

3. Butter Chicken (Punjabi Dhaba)
   Ordered: 128 times | Qty Sold: 145 | Revenue: ₹50,605

4. Pani Puri (Chat Corner)
   Ordered: 134 times | Qty Sold: 201 | Revenue: ₹11,859

5. Fish Curry (Coastal Kitchen)
   Ordered: 95 times | Qty Sold: 110 | Revenue: ₹36,190
```

**Business Value**:

- Identify most popular Indian dishes
- Inventory planning for high-demand items (Biryani, Dosa, etc.)
- Promotional campaigns for bestsellers
- Menu optimization insights
- Seasonal trend analysis

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

**Cuisine Analytics**:

```
Indian Cuisine:
  Restaurants: 3 | Orders: 156 | Revenue: ₹52,340 | Avg Rating: 4.5

South Indian:
  Restaurants: 2 | Orders: 187 | Revenue: ₹28,645 | Avg Rating: 4.5

North Indian:
  Restaurants: 2 | Orders: 145 | Revenue: ₹48,230 | Avg Rating: 4.5

Hyderabadi:
  Restaurants: 1 | Orders: 89 | Revenue: ₹29,281 | Avg Rating: 4.8

Street Food:
  Restaurants: 1 | Orders: 178 | Revenue: ₹15,602 | Avg Rating: 4.2

Seafood:
  Restaurants: 1 | Orders: 112 | Revenue: ₹36,848 | Avg Rating: 4.3
```

**Business Value**:

- Identify most demanded cuisine types in Indian market
- Expansion planning (add more South Indian/North Indian restaurants)
- Understand regional preferences (Biryani in Hyderabad, Dosa in South)
- Restaurant recruitment strategy
- Pricing analysis per cuisine type

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

## Indian Data Insights

### Popular Dishes by Category

**Biryani & Rice Dishes**: Highest revenue generators (₹250-400 per order)
**South Indian**: High volume, moderate pricing (₹60-120 per order)
**Street Food**: Maximum order frequency, lowest pricing (₹40-100)
**North Indian**: Premium pricing, consistent demand (₹250-400)
**Seafood**: Niche market, premium pricing (₹300-450)

### City-wise Distribution

**Top Cities by Customer Count**:

1. Bangalore - 12 customers
2. Mumbai - 12 customers
3. Delhi - 8 customers
4. Hyderabad - 8 customers
5. Chennai - 6 customers
6. Kolkata - 6 customers
7. Pune - 4 customers
8. Kochi - 2 customers

### Vehicle Registration Patterns

- **KA** (Karnataka) - Bangalore region
- **MH** (Maharashtra) - Mumbai region
- **DL** (Delhi) - Delhi NCR region
- **TS** (Telangana) - Hyderabad region
- **WB** (West Bengal) - Kolkata region
- **TN** (Tamil Nadu) - Chennai region
- **KL** (Kerala) - Kochi region
- **UP** (Uttar Pradesh) - North India

### Pricing Strategy

**Budget-Friendly** (₹20-100): Chai, Papad, Street Food
**Mid-Range** (₹100-250): South Indian, Thalis, Basic Curries
**Premium** (₹250-450): Biryani, North Indian, Seafood Specialties

## Testing Recommendations

1. Test each query with and without filters
2. Verify results with small data sets first
3. Check NULL handling for optional relationships
4. Validate calculations manually for accuracy
5. Test with various order status values
6. Check date comparisons across time zones
7. **Test with Indian city names and addresses**
8. **Verify vehicle registration patterns**
9. **Validate Indian currency formatting (₹)**
10. **Test vegetarian/non-vegetarian filters**

## Sample Test Queries

### Find all vegetarian dishes under ₹100

```sql
SELECT item_name, price, r.restaurant_name
FROM MenuItems m
JOIN Restaurant r ON m.restaurant_id = r.restaurant_id
WHERE m.item_type = 'veg' AND m.price < 100
ORDER BY m.price;
```

### Get orders delivered in Bangalore

```sql
SELECT o.order_id, c.customername, c.customer_address, o.total_amount
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id
WHERE c.customer_address LIKE '%Bangalore%'
AND o.order_status = 'delivered';
```

### Find delivery partners with Karnataka vehicles

```sql
SELECT name, vehicle_type, vehicle_number, phone_number
FROM DeliveryPartners
WHERE vehicle_number LIKE 'KA%';
```

### Most ordered cuisine type

```sql
SELECT r.cuisine_type, COUNT(o.order_id) as order_count
FROM Orders o
JOIN Restaurant r ON o.restaurant_id = r.restaurant_id
GROUP BY r.cuisine_type
ORDER BY order_count DESC;
```

---

**Last Updated**: October 5, 2025  
**Database**: SQLite (food_delivery.db)  
**Data Theme**: Indian Food Delivery System  
**Total Records**: 250+ sample records across 8 major Indian cities
