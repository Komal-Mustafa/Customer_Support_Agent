"""
data.py
Fake database for the Customer Support Agent.
Later this can be replaced with a real database (SQLite / Supabase).
"""

# Orders: key = order ID, value = order details
ORDERS = {
    "ORD-1001": {
        "customer_name": "Ayesha Khan",
        "email": "ayesha@example.com",
        "item": "Lawn suit (3-piece)",
        "price": 4500,
        "status": "delivered",
        "order_date": "2026-09-20",
    },
    "ORD-1002": {
        "customer_name": "Bilal Ahmed",
        "email": "bilal@example.com",
        "item": "Wireless headphones",
        "price": 6800,
        "status": "shipped",
        "order_date": "2026-10-03",
    },
    "ORD-1003": {
        "customer_name": "Sana Malik",
        "email": "sana@example.com",
        "item": "Embroidered kurta",
        "price": 3200,
        "status": "processing",
        "order_date": "2026-10-08",
    },
    "ORD-1004": {
        "customer_name": "Usman Tariq",
        "email": "usman@example.com",
        "item": "Running shoes",
        "price": 7500,
        "status": "cancelled",
        "order_date": "2026-09-28",
    },
    "ORD-1005": {
        "customer_name": "Hina Raza",
        "email": "hina@example.com",
        "item": "Mobile cover",
        "price": 800,
        "status": "refunded",
        "order_date": "2026-09-15",
    },
    "ORD-1006": {
        "customer_name": "Fahad Ali",
        "email": "fahad@example.com",
        "item": "Smart watch",
        "price": 25000,
        "status": "delivered",
        "order_date": "2026-09-25",
    },
}

# Users: for the tech support "reset password" tool
USERS = {
    "ayesha@example.com": {"name": "Ayesha Khan", "account_status": "active"},
    "bilal@example.com": {"name": "Bilal Ahmed", "account_status": "active"},
    "sana@example.com": {"name": "Sana Malik", "account_status": "locked"},
}