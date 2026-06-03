"""
mock_data.py — Fake customers, carts, and orders for demo/testing.
Replace these functions with real DB queries or API calls in production.
"""

from datetime import datetime, timedelta


def get_abandoned_carts():
    """
    Simulates pulling abandoned carts from a database.
    In production: query your Shopify/WooCommerce API or DB.
    """
    now = datetime.now()

    return [
        {
            "cart_id":        "CART-001",
            "customer_email": "erichyt873@gmail.com",
            "customer_name":  "Sarah",
            "abandoned_at":   now - timedelta(hours=2),
            "cart_value":     89.99,
            "items": [
                {"name": "Wireless Earbuds Pro", "price": 59.99, "qty": 1, "image_url": "https://placehold.co/80x80"},
                {"name": "Phone Case",            "price": 29.99, "qty": 1, "image_url": "https://placehold.co/80x80"},
            ],
            "cart_url":       "https://yourstore.com/cart/CART-001",
            "emails_sent":    [],   # track which steps have fired
        },
        {
            "cart_id":        "CART-002",
            "customer_email": "erichyt873@gmail.com",
            "customer_name":  "Mike",
            "abandoned_at":   now - timedelta(hours=26),
            "cart_value":     149.00,
            "items": [
                {"name": "Mechanical Keyboard", "price": 149.00, "qty": 1, "image_url": "https://placehold.co/80x80"},
            ],
            "cart_url":       "https://yourstore.com/cart/CART-002",
            "emails_sent":    ["step_1"],   # step 1 already sent — should get step 2
        },
        {
            "cart_id":        "CART-003",
            "customer_email": "erichyt873@gmail.com",
            "customer_name":  "Lisa",
            "abandoned_at":   now - timedelta(minutes=30),  # too recent — no email yet
            "cart_value":     45.00,
            "items": [
                {"name": "Notebook Set", "price": 45.00, "qty": 1, "image_url": "https://placehold.co/80x80"},
            ],
            "cart_url":       "https://yourstore.com/cart/CART-003",
            "emails_sent":    [],
        },
    ]


def get_recent_orders():
    """
    Simulates pulling recent orders from a database.
    In production: query your Shopify/WooCommerce API or DB.
    """
    now = datetime.now()

    return [
        {
            "order_id":       "ORD-1001",
            "customer_email": "erichyt873@gmail.com",
            "customer_name":  "Alex",
            "ordered_at":     now - timedelta(days=1, hours=1),
            "total":          120.00,
            "items":          [{"name": "Running Shoes", "qty": 1}],
            "tracking_url":   "https://yourstore.com/track/ORD-1001",
            "emails_sent":    [],
        },
        {
            "order_id":       "ORD-1002",
            "customer_email": "erichyt873@gmail.com",
            "customer_name":  "Priya",
            "ordered_at":     now - timedelta(days=3, hours=2),
            "total":          55.00,
            "items":          [{"name": "Yoga Mat", "qty": 1}],
            "tracking_url":   "https://yourstore.com/track/ORD-1002",
            "emails_sent":    ["day_1"],
        },
        {
            "order_id":       "ORD-1003",
            "customer_email": "erichyt873@gmail.com",
            "customer_name":  "James",
            "ordered_at":     now - timedelta(days=7, hours=3),
            "total":          200.00,
            "items":          [{"name": "Smart Watch", "qty": 1}],
            "tracking_url":   "https://yourstore.com/track/ORD-1003",
            "emails_sent":    ["day_1", "day_3"],
        },
    ]
