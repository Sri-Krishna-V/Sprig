// API Base URL
const API_BASE = '';

// Add number animation
function animateValue(element, start, end, duration) {
    if (!element) return;
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const value = Math.floor(progress * (end - start) + start);
        element.textContent = value;
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// Add smooth scroll
function smoothScroll() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Navigation
document.addEventListener('DOMContentLoaded', function() {
    // Hide loading screen after a short delay
    setTimeout(() => {
        const loadingScreen = document.getElementById('loadingScreen');
        if (loadingScreen) {
            loadingScreen.classList.add('hidden');
        }
    }, 800);

    // Add page load animation
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s ease';
        document.body.style.opacity = '1';
    }, 100);

    // Navigation handling
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.section');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetSection = this.dataset.section;
            
            // Smooth scroll to top
            smoothScroll();
            
            // Update active nav link with animation
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
        case 'menu':
            loadMenuItems();
            populateRestaurantFilter();
            break;
        case 'offers':
            loadOffers();
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
        
        // Animate numbers
        animateValue(document.getElementById('total-customers'), 0, data.total_customers, 1000);
        animateValue(document.getElementById('total-restaurants'), 0, data.total_restaurants, 1000);
        animateValue(document.getElementById('total-orders'), 0, data.total_orders, 1200);
        
        // Animate revenue with formatting
        const revenueEl = document.getElementById('total-revenue');
        let revenueStart = 0;
        let revenueEnd = data.total_revenue;
        let startTimestamp = null;
        const animateRevenue = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / 1500, 1);
            const value = progress * revenueEnd;
            revenueEl.textContent = `₹${formatNumber(value)}`;
            if (progress < 1) {
                window.requestAnimationFrame(animateRevenue);
            }
        };
        window.requestAnimationFrame(animateRevenue);
        
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

// ===== NEW FEATURES =====

// Menu Items
let restaurantsData = [];

async function populateRestaurantFilter() {
    try {
        const response = await fetch(`${API_BASE}/api/restaurants`);
        restaurantsData = await response.json();
        
        const filter = document.getElementById('menu-restaurant-filter');
        const orderFilter = document.getElementById('orderRestaurant');
        
        const options = restaurantsData.map(r => 
            `<option value="${r.restaurant_id}">${r.restaurant_name} - ${r.cuisine_type}</option>`
        ).join('');
        
        if (filter) filter.innerHTML += options;
        if (orderFilter) orderFilter.innerHTML += options;
    } catch (error) {
        console.error('Error loading restaurants:', error);
    }
}

async function loadMenuItems() {
    const container = document.getElementById('menu-items');
    const restaurantFilter = document.getElementById('menu-restaurant-filter').value;
    const typeFilter = document.getElementById('menu-type-filter').value;
    
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Loading menu...</div>';
    
    try {
        let url = `${API_BASE}/api/menu?`;
        if (restaurantFilter) url += `restaurant_id=${restaurantFilter}&`;
        if (typeFilter) url += `item_type=${typeFilter}`;
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.length === 0) {
            container.innerHTML = '<div class="empty-state"><i class="fas fa-utensils"></i><p>No menu items found</p></div>';
            return;
        }
        
        container.innerHTML = data.map(item => `
            <div class="menu-card">
                <div class="menu-header">
                    <h4>${item.item_name}</h4>
                    <span class="status-badge status-${item.item_type === 'veg' ? 'delivered' : 'preparing'}">
                        ${item.item_type}
                    </span>
                </div>
                <p class="menu-description">${item.description || 'Delicious item from our menu'}</p>
                <div class="menu-footer">
                    <div class="menu-restaurant">
                        <i class="fas fa-store"></i> ${item.restaurant_name}
                    </div>
                    <div class="menu-price">₹${formatNumber(item.price)}</div>
                </div>
                <div class="menu-availability ${item.availability ? 'available' : 'unavailable'}">
                    ${item.availability ? '✓ Available' : '✗ Unavailable'}
                </div>
            </div>
        `).join('');
    } catch (error) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-circle"></i><p>Error loading menu</p></div>';
    }
}

// Offers
async function loadOffers() {
    const container = document.getElementById('offers-list');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Loading offers...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/api/offers`);
        const data = await response.json();
        
        if (data.length === 0) {
            container.innerHTML = '<div class="empty-state"><i class="fas fa-tags"></i><p>No active offers available</p></div>';
            return;
        }
        
        container.innerHTML = data.map(offer => {
            const isExpired = new Date(offer.valid_to) < new Date();
            return `
                <div class="offer-card ${isExpired ? 'expired' : ''}">
                    <div class="offer-header">
                        <h4><i class="fas fa-tag"></i> ${offer.offer_code}</h4>
                        <div class="offer-discount">${offer.discount_percentage}% OFF</div>
                    </div>
                    <p class="offer-description">${offer.description || 'Get amazing discount on your order!'}</p>
                    <div class="offer-details">
                        <div class="offer-detail">
                            <i class="fas fa-shopping-cart"></i>
                            <span>Min Order: ₹${formatNumber(offer.min_order_amount)}</span>
                        </div>
                        <div class="offer-detail">
                            <i class="fas fa-calendar"></i>
                            <span>Valid: ${formatDate(offer.valid_from)}</span>
                        </div>
                        <div class="offer-detail">
                            <i class="fas fa-calendar-times"></i>
                            <span>Until: ${formatDate(offer.valid_to)}</span>
                        </div>
                    </div>
                    <div class="offer-status ${isExpired ? 'expired' : 'active'}">
                        ${isExpired ? '✗ Expired' : '✓ Active'}
                    </div>
                </div>
            `;
        }).join('');
    } catch (error) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-circle"></i><p>Error loading offers</p></div>';
    }
}

// Order Details Modal
async function showOrderDetails(orderId) {
    const modal = document.getElementById('orderModal');
    const content = document.getElementById('orderDetailsContent');
    
    modal.style.display = 'block';
    content.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Loading order details...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/api/orders/${orderId}/items`);
        const data = await response.json();
        
        if (data.length === 0) {
            content.innerHTML = '<div class="empty-state"><i class="fas fa-box-open"></i><p>No items found in this order</p></div>';
            return;
        }
        
        const order = data[0];
        const totalAmount = data.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        
        content.innerHTML = `
            <div class="order-details">
                <div class="order-info-grid">
                    <div class="order-info-item">
                        <label><i class="fas fa-hashtag"></i> Order ID:</label>
                        <span>#${order.order_id}</span>
                    </div>
                    <div class="order-info-item">
                        <label><i class="fas fa-calendar"></i> Date:</label>
                        <span>${formatDate(order.order_date)}</span>
                    </div>
                    <div class="order-info-item">
                        <label><i class="fas fa-user"></i> Customer:</label>
                        <span>${order.customername}</span>
                    </div>
                    <div class="order-info-item">
                        <label><i class="fas fa-store"></i> Restaurant:</label>
                        <span>${order.restaurant_name}</span>
                    </div>
                    <div class="order-info-item">
                        <label><i class="fas fa-motorcycle"></i> Delivery Partner:</label>
                        <span>${order.delivery_partner || 'Not assigned'}</span>
                    </div>
                    <div class="order-info-item">
                        <label><i class="fas fa-info-circle"></i> Status:</label>
                        <span class="status-badge status-${order.order_status}">${formatStatus(order.order_status)}</span>
                    </div>
                </div>
                
                <h4><i class="fas fa-list"></i> Order Items</h4>
                <table>
                    <thead>
                        <tr>
                            <th>Item</th>
                            <th>Type</th>
                            <th>Price</th>
                            <th>Quantity</th>
                            <th>Subtotal</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${data.map(item => `
                            <tr>
                                <td><strong>${item.item_name}</strong></td>
                                <td><span class="status-badge status-${item.item_type === 'veg' ? 'delivered' : 'preparing'}">${item.item_type}</span></td>
                                <td>₹${formatNumber(item.price)}</td>
                                <td>${item.quantity}</td>
                                <td>₹${formatNumber(item.price * item.quantity)}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
                
                <div class="order-summary-modal">
                    <div class="summary-row">
                        <span>Subtotal:</span>
                        <span>₹${formatNumber(totalAmount)}</span>
                    </div>
                    <div class="summary-row">
                        <span>Discount:</span>
                        <span class="highlight-success">-₹${formatNumber(order.membership_discount || 0)}</span>
                    </div>
                    <div class="summary-row total">
                        <span><strong>Total:</strong></span>
                        <span><strong>₹${formatNumber(order.total_amount)}</strong></span>
                    </div>
                </div>
                
                <div class="order-actions">
                    <button class="btn btn-primary" onclick="updateOrderStatus(${order.order_id}, 'confirmed')">
                        <i class="fas fa-check"></i> Confirm
                    </button>
                    <button class="btn btn-warning" onclick="updateOrderStatus(${order.order_id}, 'preparing')">
                        <i class="fas fa-fire"></i> Preparing
                    </button>
                    <button class="btn btn-info" onclick="updateOrderStatus(${order.order_id}, 'out_for_delivery')">
                        <i class="fas fa-shipping-fast"></i> Out for Delivery
                    </button>
                    <button class="btn btn-success" onclick="updateOrderStatus(${order.order_id}, 'delivered')">
                        <i class="fas fa-check-circle"></i> Delivered
                    </button>
                    <button class="btn btn-danger" onclick="updateOrderStatus(${order.order_id}, 'cancelled')">
                        <i class="fas fa-times-circle"></i> Cancel
                    </button>
                </div>
            </div>
        `;
    } catch (error) {
        content.innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-circle"></i><p>Error loading order details</p></div>';
    }
}

function closeOrderModal() {
    document.getElementById('orderModal').style.display = 'none';
}

// Update Order Status
async function updateOrderStatus(orderId, newStatus) {
    try {
        const response = await fetch(`${API_BASE}/api/orders/${orderId}/status`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: newStatus })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert(`Order #${orderId} status updated to: ${formatStatus(newStatus)}`);
            closeOrderModal();
            loadOrders();
        } else {
            alert('Failed to update order status: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        alert('Error updating order status: ' + error.message);
    }
}

// Create Order Modal
let selectedItems = [];
let menuItems = [];
let customers = [];
let offers = [];

async function openCreateOrderModal() {
    const modal = document.getElementById('createOrderModal');
    modal.style.display = 'block';
    
    // Load customers
    try {
        const response = await fetch(`${API_BASE}/api/customers/top-spenders`);
        customers = await response.json();
        
        const customerSelect = document.getElementById('orderCustomer');
        customerSelect.innerHTML = '<option value="">Select Customer</option>' + 
            customers.map(c => `<option value="${c.customer_id}">${c.customername} (${c.email})</option>`).join('');
    } catch (error) {
        console.error('Error loading customers:', error);
    }
    
    // Load offers
    try {
        const response = await fetch(`${API_BASE}/api/offers`);
        offers = await response.json();
        
        const offerSelect = document.getElementById('orderOffer');
        offerSelect.innerHTML = '<option value="">No Offer</option>' + 
            offers.filter(o => new Date(o.valid_to) >= new Date())
                  .map(o => `<option value="${o.offer_id}">${o.offer_code} - ${o.discount_percentage}% OFF</option>`).join('');
    } catch (error) {
        console.error('Error loading offers:', error);
    }
    
    // Populate restaurants
    await populateRestaurantFilter();
    
    // Reset form
    selectedItems = [];
    updateOrderSummary();
}

function closeCreateOrderModal() {
    document.getElementById('createOrderModal').style.display = 'none';
    document.getElementById('createOrderForm').reset();
    selectedItems = [];
}

async function loadRestaurantMenu() {
    const restaurantId = document.getElementById('orderRestaurant').value;
    const container = document.getElementById('menuItemsSelection');
    
    if (!restaurantId) {
        container.innerHTML = '<p class="text-muted">Select a restaurant to view menu</p>';
        return;
    }
    
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Loading menu...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/api/menu?restaurant_id=${restaurantId}`);
        menuItems = await response.json();
        
        if (menuItems.length === 0) {
            container.innerHTML = '<p class="text-muted">No menu items available</p>';
            return;
        }
        
        container.innerHTML = menuItems.filter(item => item.availability).map(item => `
            <div class="menu-item-selector">
                <div class="menu-item-info">
                    <span class="menu-item-name">${item.item_name}</span>
                    <span class="menu-item-price">₹${formatNumber(item.price)}</span>
                </div>
                <div class="menu-item-actions">
                    <button type="button" class="btn-sm" onclick="removeMenuItem(${item.menu_item_id})">-</button>
                    <input type="number" id="qty-${item.menu_item_id}" value="0" min="0" class="qty-input" onchange="updateMenuItem(${item.menu_item_id}, this.value)">
                    <button type="button" class="btn-sm" onclick="addMenuItem(${item.menu_item_id})">+</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        container.innerHTML = '<p class="text-danger">Error loading menu</p>';
    }
}

function addMenuItem(itemId) {
    const qtyInput = document.getElementById(`qty-${itemId}`);
    qtyInput.value = parseInt(qtyInput.value) + 1;
    updateMenuItem(itemId, qtyInput.value);
}

function removeMenuItem(itemId) {
    const qtyInput = document.getElementById(`qty-${itemId}`);
    const newQty = Math.max(0, parseInt(qtyInput.value) - 1);
    qtyInput.value = newQty;
    updateMenuItem(itemId, newQty);
}

function updateMenuItem(itemId, quantity) {
    const qty = parseInt(quantity);
    const existingIndex = selectedItems.findIndex(item => item.menu_item_id === itemId);
    
    if (qty > 0) {
        const menuItem = menuItems.find(item => item.menu_item_id === itemId);
        if (existingIndex >= 0) {
            selectedItems[existingIndex].quantity = qty;
        } else {
            selectedItems.push({
                menu_item_id: itemId,
                item_name: menuItem.item_name,
                price: menuItem.price,
                quantity: qty
            });
        }
    } else {
        if (existingIndex >= 0) {
            selectedItems.splice(existingIndex, 1);
        }
    }
    
    updateOrderSummary();
}

function updateOrderSummary() {
    const summaryContainer = document.getElementById('orderSummaryItems');
    const totalContainer = document.getElementById('orderTotal');
    
    if (selectedItems.length === 0) {
        summaryContainer.innerHTML = '<p class="text-muted">No items selected</p>';
        totalContainer.textContent = '0';
        return;
    }
    
    summaryContainer.innerHTML = selectedItems.map(item => `
        <div class="summary-item">
            <span>${item.item_name} x${item.quantity}</span>
            <span>₹${formatNumber(item.price * item.quantity)}</span>
        </div>
    `).join('');
    
    const total = selectedItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    totalContainer.textContent = formatNumber(total);
}

// Handle Create Order Form Submission
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('createOrderForm');
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            if (selectedItems.length === 0) {
                alert('Please select at least one menu item');
                return;
            }
            
            const customerId = document.getElementById('orderCustomer').value;
            const restaurantId = document.getElementById('orderRestaurant').value;
            const offerId = document.getElementById('orderOffer').value || null;
            const paymentMethod = document.getElementById('orderPaymentMethod').value;
            const deliveryAddress = document.getElementById('deliveryAddress').value;
            
            const orderData = {
                customer_id: parseInt(customerId),
                restaurant_id: parseInt(restaurantId),
                items: selectedItems,
                offer_id: offerId ? parseInt(offerId) : null,
                payment_method: paymentMethod,
                delivery_address: deliveryAddress
            };
            
            try {
                const response = await fetch(`${API_BASE}/api/orders/create`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(orderData)
                });
                
                const data = await response.json();
                
                if (data.success) {
                    alert(`Order created successfully! Order ID: #${data.order_id}`);
                    closeCreateOrderModal();
                    loadOrders();
                } else {
                    alert('Failed to create order: ' + (data.error || 'Unknown error'));
                }
            } catch (error) {
                alert('Error creating order: ' + error.message);
            }
        });
    }
});

// Make orders clickable
async function loadOrders() {
    const container = document.getElementById('orders-list');
    const status = document.getElementById('order-status-filter').value;
    const dateFrom = document.getElementById('order-date-from')?.value;
    const dateTo = document.getElementById('order-date-to')?.value;
    const sort = document.getElementById('order-sort')?.value || 'date_desc';
    
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Loading orders...</div>';
    
    try {
        const url = status ? `${API_BASE}/api/orders?status=${status}` : `${API_BASE}/api/orders`;
        const response = await fetch(url);
        let data = await response.json();
        
        // Filter by date range
        if (dateFrom) {
            data = data.filter(o => new Date(o.order_date) >= new Date(dateFrom));
        }
        if (dateTo) {
            const toDate = new Date(dateTo);
            toDate.setHours(23, 59, 59);
            data = data.filter(o => new Date(o.order_date) <= toDate);
        }
        
        // Sort data
        switch(sort) {
            case 'date_desc':
                data.sort((a, b) => new Date(b.order_date) - new Date(a.order_date));
                break;
            case 'date_asc':
                data.sort((a, b) => new Date(a.order_date) - new Date(b.order_date));
                break;
            case 'amount_desc':
                data.sort((a, b) => b.total_amount - a.total_amount);
                break;
            case 'amount_asc':
                data.sort((a, b) => a.total_amount - b.total_amount);
                break;
        }
        
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
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.map(o => `
                        <tr class="order-row" onclick="showOrderDetails(${o.order_id})">
                            <td><strong>#${o.order_id}</strong></td>
                            <td>${formatDate(o.order_date)}</td>
                            <td>${o.customername}<br><small>${o.customer_email}</small></td>
                            <td>${o.restaurant_name}<br><small>${o.cuisine_type}</small></td>
                            <td>${o.delivery_partner || 'Not assigned'}</td>
                            <td class="highlight-success">₹${formatNumber(o.total_amount)}</td>
                            <td>₹${formatNumber(o.membership_discount)}</td>
                            <td>${o.payment_method || 'N/A'}<br><small>${o.payment_status || 'N/A'}</small></td>
                            <td><span class="status-badge status-${o.order_status}">${formatStatus(o.order_status)}</span></td>
                            <td><button class="btn-sm btn-primary" onclick="event.stopPropagation(); showOrderDetails(${o.order_id})"><i class="fas fa-eye"></i></button></td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } catch (error) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-circle"></i><p>Error loading orders</p></div>';
    }
}

// Global Search
let searchTimeout;
function handleGlobalSearch(event) {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        const searchTerm = event.target.value.toLowerCase().trim();
        
        if (!searchTerm) {
            // Reload current section data
            const activeSection = document.querySelector('.section.active');
            if (activeSection) {
                loadSectionData(activeSection.id);
            }
            return;
        }
        
        // Get active section
        const activeSection = document.querySelector('.section.active');
        if (!activeSection) return;
        
        // Search based on active section
        switch(activeSection.id) {
            case 'orders':
                searchOrders(searchTerm);
                break;
            case 'restaurants':
                searchRestaurants(searchTerm);
                break;
            case 'customers':
                searchCustomers(searchTerm);
                break;
            case 'menu':
                searchMenu(searchTerm);
                break;
            default:
                break;
        }
    }, 300);
}

async function searchOrders(searchTerm) {
    const container = document.getElementById('orders-list');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Searching...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/api/orders`);
        let data = await response.json();
        
        // Filter by search term
        data = data.filter(o => 
            o.order_id.toString().includes(searchTerm) ||
            o.customername.toLowerCase().includes(searchTerm) ||
            o.customer_email.toLowerCase().includes(searchTerm) ||
            o.restaurant_name.toLowerCase().includes(searchTerm) ||
            (o.delivery_partner && o.delivery_partner.toLowerCase().includes(searchTerm))
        );
        
        if (data.length === 0) {
            container.innerHTML = `<div class="empty-state"><i class="fas fa-search"></i><p>No orders found matching "${searchTerm}"</p></div>`;
            return;
        }
        
        // Display results (reuse the same table structure)
        container.innerHTML = `
            <div class="search-results-header">
                <p>Found ${data.length} order(s) matching "${searchTerm}"</p>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Order ID</th>
                        <th>Date</th>
                        <th>Customer</th>
                        <th>Restaurant</th>
                        <th>Delivery Partner</th>
                        <th>Amount</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.map(o => `
                        <tr class="order-row" onclick="showOrderDetails(${o.order_id})">
                            <td><strong>#${o.order_id}</strong></td>
                            <td>${formatDate(o.order_date)}</td>
                            <td>${o.customername}<br><small>${o.customer_email}</small></td>
                            <td>${o.restaurant_name}</td>
                            <td>${o.delivery_partner || 'Not assigned'}</td>
                            <td class="highlight-success">₹${formatNumber(o.total_amount)}</td>
                            <td><span class="status-badge status-${o.order_status}">${formatStatus(o.order_status)}</span></td>
                            <td><button class="btn-sm btn-primary" onclick="event.stopPropagation(); showOrderDetails(${o.order_id})"><i class="fas fa-eye"></i></button></td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } catch (error) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-circle"></i><p>Error searching orders</p></div>';
    }
}

async function searchRestaurants(searchTerm) {
    const container = document.getElementById('restaurants-list');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Searching...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/api/restaurants`);
        let data = await response.json();
        
        data = data.filter(r => 
            r.restaurant_name.toLowerCase().includes(searchTerm) ||
            r.cuisine_type.toLowerCase().includes(searchTerm) ||
            r.restaurant_address.toLowerCase().includes(searchTerm)
        );
        
        if (data.length === 0) {
            container.innerHTML = `<div class="empty-state"><i class="fas fa-search"></i><p>No restaurants found matching "${searchTerm}"</p></div>`;
            return;
        }
        
        container.innerHTML = `
            <div class="search-results-header">
                <p>Found ${data.length} restaurant(s) matching "${searchTerm}"</p>
            </div>
        ` + data.map(r => `
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
                    <div><i class="fas fa-utensils"></i> ${r.menu_items_count} menu items</div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-circle"></i><p>Error searching restaurants</p></div>';
    }
}

async function searchCustomers(searchTerm) {
    const container = document.getElementById('spenders-table');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Searching...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/api/customers/top-spenders`);
        let data = await response.json();
        
        data = data.filter(c => 
            c.customername.toLowerCase().includes(searchTerm) ||
            c.email.toLowerCase().includes(searchTerm)
        );
        
        if (data.length === 0) {
            container.innerHTML = `<div class="empty-state"><i class="fas fa-search"></i><p>No customers found matching "${searchTerm}"</p></div>`;
            return;
        }
        
        container.innerHTML = `
            <div class="search-results-header">
                <p>Found ${data.length} customer(s) matching "${searchTerm}"</p>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Customer Name</th>
                        <th>Email</th>
                        <th>Membership</th>
                        <th>Total Orders</th>
                        <th>Total Spent</th>
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
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } catch (error) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-circle"></i><p>Error searching customers</p></div>';
    }
}

async function searchMenu(searchTerm) {
    const container = document.getElementById('menu-items');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Searching...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/api/menu`);
        let data = await response.json();
        
        data = data.filter(item => 
            item.item_name.toLowerCase().includes(searchTerm) ||
            item.restaurant_name.toLowerCase().includes(searchTerm) ||
            (item.description && item.description.toLowerCase().includes(searchTerm))
        );
        
        if (data.length === 0) {
            container.innerHTML = `<div class="empty-state"><i class="fas fa-search"></i><p>No menu items found matching "${searchTerm}"</p></div>`;
            return;
        }
        
        container.innerHTML = `
            <div class="search-results-header">
                <p>Found ${data.length} menu item(s) matching "${searchTerm}"</p>
            </div>
        ` + data.map(item => `
            <div class="menu-card">
                <div class="menu-header">
                    <h4>${item.item_name}</h4>
                    <span class="status-badge status-${item.item_type === 'veg' ? 'delivered' : 'preparing'}">
                        ${item.item_type}
                    </span>
                </div>
                <p class="menu-description">${item.description || 'Delicious item from our menu'}</p>
                <div class="menu-footer">
                    <div class="menu-restaurant">
                        <i class="fas fa-store"></i> ${item.restaurant_name}
                    </div>
                    <div class="menu-price">₹${formatNumber(item.price)}</div>
                </div>
                <div class="menu-availability ${item.availability ? 'available' : 'unavailable'}">
                    ${item.availability ? '✓ Available' : '✗ Unavailable'}
                </div>
            </div>
        `).join('');
    } catch (error) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-circle"></i><p>Error searching menu</p></div>';
    }
}

// Close modals when clicking outside
window.onclick = function(event) {
    const orderModal = document.getElementById('orderModal');
    const createModal = document.getElementById('createOrderModal');
    
    if (event.target == orderModal) {
        closeOrderModal();
    }
    if (event.target == createModal) {
        closeCreateOrderModal();
    }
}
