// API Base URL
const API_BASE = '';

// Navigation
document.addEventListener('DOMContentLoaded', function() {
    // Navigation handling
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.section');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetSection = this.dataset.section;
            
            // Update active nav link
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            
            // Show target section
            sections.forEach(s => s.classList.remove('active'));
            document.getElementById(targetSection).classList.add('active');
            
            // Load section data
            loadSectionData(targetSection);
        });
    });
    
    // Tab handling
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const targetTab = this.dataset.tab;
            const parent = this.closest('.section');
            
            // Update active tab button
            parent.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Show target tab pane
            parent.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
            parent.querySelector(`#${targetTab}`).classList.add('active');
            
            // Load tab data
            loadTabData(targetTab);
        });
    });
    
    // Initial load
    loadDashboard();
});

// Load section data based on which section is active
function loadSectionData(section) {
    switch(section) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'restaurants':
            loadRestaurants();
            break;
        case 'orders':
            loadOrders();
            break;
        case 'analytics':
            loadRevenueAnalytics();
            break;
        case 'customers':
            loadTopSpenders();
            break;
    }
}

// Load tab data
function loadTabData(tab) {
    switch(tab) {
        case 'revenue':
            loadRevenueAnalytics();
            break;
        case 'delivery':
            loadDeliveryPerformance();
            break;
        case 'popular':
            loadPopularItems();
            break;
        case 'payment':
            loadPaymentAnalysis();
            break;
        case 'cuisine':
            loadCuisineStats();
            break;
        case 'spenders':
            loadTopSpenders();
            break;
        case 'membership':
            loadMembershipCustomers();
            break;
    }
}

// Dashboard
async function loadDashboard() {
    try {
        // Load summary stats
        const response = await fetch(`${API_BASE}/api/dashboard/summary`);
        const data = await response.json();
        
        document.getElementById('total-customers').textContent = data.total_customers;
        document.getElementById('total-restaurants').textContent = data.total_restaurants;
        document.getElementById('total-orders').textContent = data.total_orders;
        document.getElementById('total-revenue').textContent = `₹${formatNumber(data.total_revenue)}`;
        
        // Load top restaurants
        loadTopRestaurants();
        
        // Load recent orders
        loadRecentOrders();
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

async function loadTopRestaurants() {
    const container = document.getElementById('top-restaurants');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Loading...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/api/analytics/restaurant-revenue`);
        const data = await response.json();
        
        const top5 = data.slice(0, 5);
        
        container.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Restaurant</th>
                        <th>Orders</th>
                        <th>Revenue</th>
                        <th>Success Rate</th>
                    </tr>
                </thead>
                <tbody>
                    ${top5.map(r => `
                        <tr>
                            <td><strong>${r.restaurant_name}</strong><br><small>${r.cuisine_type}</small></td>
                            <td>${r.total_orders || 0}</td>
                            <td class="highlight-success">₹${formatNumber(r.total_revenue || 0)}</td>
                            <td>${r.success_rate || 0}%</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } catch (error) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-circle"></i><p>Error loading data</p></div>';
    }
}

async function loadRecentOrders() {
    const container = document.getElementById('recent-orders');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Loading...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/api/orders`);
        const data = await response.json();
        
        const recent = data.slice(0, 5);
        
        container.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Order ID</th>
                        <th>Customer</th>
                        <th>Restaurant</th>
                        <th>Amount</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    ${recent.map(o => `
                        <tr>
                            <td>#${o.order_id}</td>
                            <td>${o.customername}</td>
                            <td>${o.restaurant_name}</td>
                            <td>₹${formatNumber(o.total_amount)}</td>
                            <td><span class="status-badge status-${o.order_status}">${formatStatus(o.order_status)}</span></td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } catch (error) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-circle"></i><p>Error loading data</p></div>';
    }
}

// Restaurants
async function loadRestaurants() {
    const container = document.getElementById('restaurants-list');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Loading restaurants...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/api/restaurants`);
        const data = await response.json();
        
        if (data.length === 0) {
            container.innerHTML = '<div class="empty-state"><i class="fas fa-store-slash"></i><p>No restaurants found</p></div>';
            return;
        }
        
        container.innerHTML = data.map(r => `
            <div class="restaurant-card">
                <div class="restaurant-header">
                    <div>
                        <div class="restaurant-name">${r.restaurant_name}</div>
                        <div class="restaurant-cuisine">${r.cuisine_type}</div>
                    </div>
                    <div class="restaurant-rating">
                        <i class="fas fa-star"></i>
                        ${r.rating}
                    </div>
                </div>
                <div class="restaurant-info">
                    <div><i class="fas fa-map-marker-alt"></i> ${r.restaurant_address}</div>
                    <div><i class="fas fa-user"></i> Owner: ${r.owner_name}</div>
                    <div><i class="fas fa-utensils"></i> ${r.menu_items_count} menu items</div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-circle"></i><p>Error loading restaurants</p></div>';
    }
}

// Orders
async function loadOrders() {
    const container = document.getElementById('orders-list');
    const status = document.getElementById('order-status-filter').value;
    
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Loading orders...</div>';
    
    try {
        const url = status ? `${API_BASE}/api/orders?status=${status}` : `${API_BASE}/api/orders`;
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.length === 0) {
            container.innerHTML = '<div class="empty-state"><i class="fas fa-shopping-cart"></i><p>No orders found</p></div>';
            return;
        }
        
        container.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Order ID</th>
                        <th>Date</th>
                        <th>Customer</th>
                        <th>Restaurant</th>
                        <th>Delivery Partner</th>
                        <th>Amount</th>
                        <th>Discount</th>
                        <th>Payment</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.map(o => `
                        <tr>
                            <td><strong>#${o.order_id}</strong></td>
                            <td>${formatDate(o.order_date)}</td>
                            <td>${o.customername}<br><small>${o.customer_email}</small></td>
                            <td>${o.restaurant_name}<br><small>${o.cuisine_type}</small></td>
                            <td>${o.delivery_partner || 'Not assigned'}</td>
                            <td class="highlight-success">₹${formatNumber(o.total_amount)}</td>
                            <td>₹${formatNumber(o.membership_discount)}</td>
                            <td>${o.payment_method || 'N/A'}<br><small>${o.payment_status || 'N/A'}</small></td>
                            <td><span class="status-badge status-${o.order_status}">${formatStatus(o.order_status)}</span></td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } catch (error) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-circle"></i><p>Error loading orders</p></div>';
    }
}

// Analytics - Revenue
async function loadRevenueAnalytics() {
    const container = document.getElementById('revenue-table');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Loading...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/api/analytics/restaurant-revenue`);
        const data = await response.json();
        
        container.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Restaurant</th>
                        <th>Cuisine</th>
                        <th>Total Orders</th>
                        <th>Delivered Orders</th>
                        <th>Total Revenue</th>
                        <th>Avg Order Value</th>
                        <th>Success Rate</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.map(r => `
                        <tr>
                            <td><strong>${r.restaurant_name}</strong></td>
                            <td>${r.cuisine_type}</td>
                            <td>${r.total_orders || 0}</td>
                            <td>${r.delivered_orders || 0}</td>
                            <td class="highlight-success">₹${formatNumber(r.total_revenue || 0)}</td>
                            <td>₹${formatNumber(r.avg_order_value || 0)}</td>
                            <td><span class="highlight-number">${r.success_rate || 0}%</span></td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } catch (error) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-circle"></i><p>Error loading data</p></div>';
    }
}

// Analytics - Delivery Performance
async function loadDeliveryPerformance() {
    const container = document.getElementById('delivery-table');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Loading...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/api/analytics/delivery-performance`);
        const data = await response.json();
        
        container.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Partner Name</th>
                        <th>Vehicle Type</th>
                        <th>Total Deliveries</th>
                        <th>Completed</th>
                        <th>Total Order Value</th>
                        <th>Avg Order Value</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.map(d => `
                        <tr>
                            <td><strong>${d.name}</strong></td>
                            <td>${d.vehicle_type}</td>
                            <td>${d.total_deliveries || 0}</td>
                            <td class="highlight-success">${d.completed_deliveries || 0}</td>
                            <td>₹${formatNumber(d.total_order_value || 0)}</td>
                            <td>₹${formatNumber(d.avg_order_value || 0)}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } catch (error) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-circle"></i><p>Error loading data</p></div>';
    }
}

// Analytics - Popular Items
async function loadPopularItems() {
    const container = document.getElementById('popular-table');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Loading...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/api/analytics/popular-items`);
        const data = await response.json();
        
        container.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Item Name</th>
                        <th>Restaurant</th>
                        <th>Type</th>
                        <th>Price</th>
                        <th>Times Ordered</th>
                        <th>Total Quantity</th>
                        <th>Total Revenue</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.map(item => `
                        <tr>
                            <td><strong>${item.item_name}</strong></td>
                            <td>${item.restaurant_name}</td>
                            <td><span class="status-badge status-${item.item_type === 'veg' ? 'delivered' : 'preparing'}">${item.item_type}</span></td>
                            <td>₹${formatNumber(item.price)}</td>
                            <td class="highlight-number">${item.times_ordered}</td>
                            <td>${item.total_quantity_sold}</td>
                            <td class="highlight-success">₹${formatNumber(item.total_revenue)}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } catch (error) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-circle"></i><p>Error loading data</p></div>';
    }
}

// Analytics - Payment Methods
async function loadPaymentAnalysis() {
    const container = document.getElementById('payment-table');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Loading...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/api/analytics/payment-methods`);
        const data = await response.json();
        
        container.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Payment Method</th>
                        <th>Total Transactions</th>
                        <th>Total Amount</th>
                        <th>Avg Transaction</th>
                        <th>Successful</th>
                        <th>Failed</th>
                        <th>Success Rate</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.map(p => {
                        const successRate = (p.successful_transactions / p.transaction_count * 100).toFixed(2);
                        return `
                            <tr>
                                <td><strong>${p.payment_method.toUpperCase()}</strong></td>
                                <td>${p.transaction_count}</td>
                                <td class="highlight-success">₹${formatNumber(p.total_amount)}</td>
                                <td>₹${formatNumber(p.avg_transaction)}</td>
                                <td class="highlight-success">${p.successful_transactions}</td>
                                <td class="highlight-danger">${p.failed_transactions}</td>
                                <td><span class="highlight-number">${successRate}%</span></td>
                            </tr>
                        `;
                    }).join('')}
                </tbody>
            </table>
        `;
    } catch (error) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-circle"></i><p>Error loading data</p></div>';
    }
}

// Analytics - Cuisine Stats
async function loadCuisineStats() {
    const container = document.getElementById('cuisine-table');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Loading...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/api/analytics/cuisine-stats`);
        const data = await response.json();
        
        container.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Cuisine Type</th>
                        <th>Restaurants</th>
                        <th>Total Orders</th>
                        <th>Total Revenue</th>
                        <th>Avg Restaurant Rating</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.map(c => `
                        <tr>
                            <td><strong>${c.cuisine_type}</strong></td>
                            <td>${c.restaurant_count}</td>
                            <td>${c.total_orders || 0}</td>
                            <td class="highlight-success">₹${formatNumber(c.total_revenue || 0)}</td>
                            <td><span class="highlight-number">${(c.avg_rating || 0).toFixed(1)} ⭐</span></td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } catch (error) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-circle"></i><p>Error loading data</p></div>';
    }
}

// Customers - Top Spenders
async function loadTopSpenders() {
    const container = document.getElementById('spenders-table');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Loading...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/api/customers/top-spenders`);
        const data = await response.json();
        
        container.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Customer Name</th>
                        <th>Email</th>
                        <th>Membership</th>
                        <th>Total Orders</th>
                        <th>Total Spent</th>
                        <th>Avg Order Value</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.map(c => `
                        <tr>
                            <td><strong>${c.customername}</strong></td>
                            <td>${c.email}</td>
                            <td><span class="status-badge status-${c.membership_type ? 'delivered' : 'pending'}">${c.membership_type || 'None'}</span></td>
                            <td>${c.total_orders}</td>
                            <td class="highlight-success">₹${formatNumber(c.total_spent)}</td>
                            <td>₹${formatNumber(c.avg_order_value)}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } catch (error) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-circle"></i><p>Error loading data</p></div>';
    }
}

// Customers - Membership
async function loadMembershipCustomers() {
    const container = document.getElementById('membership-table');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Loading...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/api/customers/membership`);
        const data = await response.json();
        
        container.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Customer Name</th>
                        <th>Email</th>
                        <th>Membership Type</th>
                        <th>Discount Rate</th>
                        <th>Expiry Date</th>
                        <th>Total Orders</th>
                        <th>Total Savings</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.map(c => `
                        <tr>
                            <td><strong>${c.customername}</strong></td>
                            <td>${c.email}</td>
                            <td><span class="status-badge status-delivered">${c.membership_type}</span></td>
                            <td class="highlight-number">${c.discount_rate}%</td>
                            <td>${formatDate(c.expiry_date)}</td>
                            <td>${c.total_orders}</td>
                            <td class="highlight-success">₹${formatNumber(c.total_savings || 0)}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } catch (error) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-circle"></i><p>Error loading data</p></div>';
    }
}

// Utility Functions
function formatNumber(num) {
    return parseFloat(num || 0).toFixed(2);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatStatus(status) {
    return status.split('_').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
}
