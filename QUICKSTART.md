# Quick Start Guide

## 🚀 Getting Started (3 Easy Steps)

### Step 1: Install Flask
```powershell
pip install flask
```

### Step 2: Initialize Database
```powershell
python populate_data.py
```

### Step 3: Start the Application
```powershell
python app.py
```

Then open your browser to: **http://localhost:5000**

---

## 📦 Alternative: Use Setup Script

Double-click `setup.bat` to automatically:
- Install Flask
- Create database
- Populate sample data

Then double-click `run.bat` to start the server.

---

## 🎯 What's Included

### ✅ Database (food_delivery.db)
- 13 tables with proper relationships
- Sample data:
  - 8 customers
  - 6 restaurants (Italian, American, Japanese, Mexican, Indian)
  - 25+ menu items
  - 5 delivery partners
  - 8 orders with complete details

### ✅ Backend (app.py)
- 12+ API endpoints
- 10 complex SQL queries
- RESTful architecture
- JSON responses

### ✅ Frontend
- Modern gradient-based UI
- Responsive design
- 5 main sections:
  1. Dashboard (overview stats)
  2. Restaurants (browse all restaurants)
  3. Orders (order management)
  4. Analytics (5 different reports)
  5. Customers (customer insights)

---

## 📊 10 Key Queries You Can See

1. **Restaurant Listing** - All restaurants with menu counts
2. **Top Spenders** - Customers ranked by spending
3. **Menu Items** - Browse items with filters
4. **Order Details** - Complete order tracking
5. **Revenue Analysis** - Restaurant performance metrics
6. **Delivery Performance** - Partner efficiency tracking
7. **Popular Items** - Bestselling menu items
8. **Membership Analysis** - Customer savings tracking
9. **Payment Methods** - Payment preference analytics
10. **Cuisine Stats** - Performance by cuisine type

---

## 🎨 Features Showcase

### Dashboard
- Total customers, restaurants, orders, revenue
- Top 5 performing restaurants
- Recent orders list

### Restaurants Page
- Restaurant cards with ratings
- Cuisine types and addresses
- Menu item counts

### Orders Page
- Filter by status (pending, delivered, etc.)
- Complete order details
- Payment and delivery information

### Analytics Page
5 Different Reports:
- 📈 Revenue Analysis
- 🚚 Delivery Performance
- ⭐ Popular Items
- 💳 Payment Methods
- 🍽️ Cuisine Statistics

### Customers Page
- Top spenders list
- Membership benefits
- Order history

---

## 🔧 Troubleshooting

### "Module not found: flask"
```powershell
pip install flask
```

### "No such file: food_delivery.db"
```powershell
python populate_data.py
```

### "Port 5000 already in use"
Edit `app.py` line 303:
```python
app.run(debug=True, port=5001)  # Change port
```

### Application won't start
Check Python version:
```powershell
python --version
```
Requires Python 3.7+

---

## 📱 Navigation Guide

### Using the Application

1. **Top Navigation Bar**: Click any menu item to switch sections
   - Dashboard 🏠
   - Restaurants 🏪
   - Orders 🛒
   - Analytics 📊
   - Customers 👥

2. **Filters & Refresh**: Use dropdown filters and refresh buttons

3. **Tables**: All data is displayed in sortable tables

4. **Status Badges**: Color-coded for easy identification
   - 🟡 Pending
   - 🔵 Confirmed
   - 🟣 Preparing
   - 🟢 Delivered
   - 🔴 Cancelled

---

## 💡 Pro Tips

### For Presentation
1. Start with Dashboard to show overview
2. Navigate to Restaurants to show data
3. Go to Analytics → Revenue to show complex queries
4. Show Popular Items for business insights
5. End with Top Spenders to show customer analysis

### For Development
- Check `QUERIES.md` for detailed SQL query explanations
- Backend: `app.py` contains all API endpoints
- Frontend: `static/script.js` contains fetch logic
- Database: `database_schema.sql` shows complete schema

### For Testing
- Use different order status filters
- Check empty states (data without orders)
- Test responsive design (resize browser)
- Inspect network tab to see API calls

---

## 📁 File Structure

```
Sprig/
│
├── app.py                    # Flask backend
├── populate_data.py         # Database setup
├── database_schema.sql      # Schema definition
├── food_delivery.db         # SQLite database
│
├── templates/
│   └── index.html           # Main page
│
├── static/
│   ├── style.css            # Styles
│   └── script.js            # Frontend logic
│
├── setup.bat                # Auto setup script
├── run.bat                  # Quick start script
├── requirements.txt         # Dependencies
├── README.md                # Full documentation
├── QUERIES.md               # Query explanations
└── QUICKSTART.md            # This file
```

---

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ Converting ER diagrams to database schemas
- ✅ Complex SQL queries (joins, aggregations, subqueries)
- ✅ RESTful API design
- ✅ Frontend-backend integration
- ✅ Modern UI/UX design
- ✅ Data visualization
- ✅ Professional code organization

---

## 📞 Common Questions

**Q: Can I modify the data?**  
A: Yes! Edit `populate_data.py` and run it again.

**Q: How do I add more queries?**  
A: Add a route in `app.py`, then call it from `script.js`.

**Q: Can I use MySQL/PostgreSQL instead?**  
A: Yes, but you'll need to modify connection code and some SQL syntax.

**Q: Is this production-ready?**  
A: No, this is for educational purposes. Add authentication, validation, error handling for production.

**Q: Can I deploy this online?**  
A: Yes, use platforms like Heroku, PythonAnywhere, or AWS.

---

## 🌟 Next Steps

1. ✅ Run the application
2. ✅ Explore all sections
3. ✅ Read `QUERIES.md` for query details
4. ✅ Customize the design in `style.css`
5. ✅ Add your own queries
6. ✅ Present to your class!

---

**Enjoy exploring the Food Delivery Management System! 🍕🍔🍣**
