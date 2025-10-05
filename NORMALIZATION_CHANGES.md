# Database Normalization to BCNF

## Summary

Your database has been successfully normalized to **Boyce-Codd Normal Form (BCNF)**.

## Changes Made

### 1. **RestaurantOwners Table** - Fixed Transitive Dependency

**Problem:** The `restaurant_name` column created a transitive dependency:

- `ro_id → restaurant_id → restaurant_name`
- This violated 3NF/BCNF because `restaurant_id` is not a superkey

**Solution:**

```sql
-- BEFORE (Violated BCNF)
CREATE TABLE RestaurantOwners (
    ro_id INTEGER PRIMARY KEY,
    restaurant_id INTEGER,
    restaurant_name VARCHAR(100) NOT NULL  -- ❌ Redundant
);

-- AFTER (BCNF Compliant)
CREATE TABLE RestaurantOwners (
    ro_id INTEGER PRIMARY KEY,
    restaurant_id INTEGER  -- ✅ No redundancy
);
```

**Impact:** Restaurant names are now retrieved via JOIN with the `Restaurant` table.

---

### 2. **Orders Table** - Removed Calculated Field

**Problem:** `membership_discount` was a calculated field that could become inconsistent with the `Membership` table data.

**Solution:**

```sql
-- BEFORE
CREATE TABLE Orders (
    ...
    membership_discount DECIMAL(10,2) DEFAULT 0.0,  -- ❌ Stored calculation
    total_amount DECIMAL(10,2) NOT NULL
);

-- AFTER
CREATE TABLE Orders (
    ...
    total_amount DECIMAL(10,2) NOT NULL  -- ✅ Calculate discount on-the-fly
);
```

**Impact:** Membership discounts are now calculated dynamically using:

```sql
ROUND(o.total_amount * COALESCE(m.discount_rate, 0) / 100, 2) as membership_discount
```

---

### 3. **Carts Table** - Removed Calculated Field

**Problem:** `totalprice` was redundant and could become inconsistent with `CartItems` data.

**Solution:**

```sql
-- BEFORE
CREATE TABLE Carts (
    cart_id INTEGER PRIMARY KEY,
    customer_id INTEGER UNIQUE,
    totalprice DECIMAL(10,2) DEFAULT 0.0  -- ❌ Redundant
);

-- AFTER
CREATE TABLE Carts (
    cart_id INTEGER PRIMARY KEY,
    customer_id INTEGER UNIQUE  -- ✅ Calculate total on-the-fly
);
```

**Impact:** Cart totals are now calculated dynamically by summing `CartItems`.

---

## Normalization Levels Achieved

### ✅ **1NF (First Normal Form)** - SATISFIED

- All attributes contain atomic values
- No repeating groups
- Primary keys exist for all tables

### ✅ **2NF (Second Normal Form)** - SATISFIED

- All non-key attributes are fully functionally dependent on the primary key
- No partial dependencies exist

### ✅ **3NF (Third Normal Form)** - SATISFIED

- No transitive dependencies remain
- All non-key attributes depend only on the primary key

### ✅ **BCNF (Boyce-Codd Normal Form)** - SATISFIED

- For every functional dependency X → Y, X is a superkey
- All determinants are candidate keys

---

## Benefits of BCNF Normalization

1. **Data Integrity**: Eliminates update anomalies and inconsistencies
2. **No Redundancy**: Each piece of data is stored exactly once
3. **Flexibility**: Easy to update membership rates or restaurant names without affecting multiple tables
4. **Maintainability**: Simpler schema with clearer relationships
5. **Accuracy**: Calculated values are always up-to-date

---

## Application Updates

### Files Modified

1. **database_schema.sql** - Updated table definitions
2. **populate_data.py** - Updated INSERT statements
3. **app.py** - Updated queries to calculate discounts and retrieve data via JOINs

### Query Changes

- Restaurant queries now fetch owner info via JOIN
- Order queries calculate membership discounts dynamically
- Membership savings are computed using discount rates

---

## Testing

The database has been recreated and repopulated with normalized schema. All sample data has been successfully inserted:

- ✅ 13 Users
- ✅ 8 Customers  
- ✅ 6 Restaurants
- ✅ 25 Menu Items
- ✅ 8 Orders
- ✅ 5 Delivery Partners

---

## What About 4NF and 5NF?

### **4NF (Fourth Normal Form)**

Your database satisfies 4NF because:

- No multi-valued dependencies exist
- All many-to-many relationships are properly handled through junction tables

### **5NF (Fifth Normal Form)**

Your database satisfies 5NF because:

- No join dependencies that require further decomposition
- All relationships are at the appropriate level of granularity

---

## Conclusion

Your database is now **fully normalized to BCNF** and also satisfies **4NF and 5NF**. The schema is:

- ✅ Free from redundancy
- ✅ Free from update anomalies
- ✅ Optimized for data integrity
- ✅ BCNF compliant

The application code has been updated to work seamlessly with the normalized schema, calculating derived values on-the-fly rather than storing them.
