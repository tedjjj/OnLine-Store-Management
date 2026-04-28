import sqlite3
from datetime import datetime


def search_product(product_name: str, size: str = None, color: str = None) -> str:

    conn = sqlite3.connect("store.db")

    # Build query based on what info we have
    if size and color:
        # search by name + size + color
        cursor = conn.execute("""
            SELECT name, size, color, quantity, price
            FROM products
            WHERE name LIKE ? AND size = ? AND color = ?
        """, (f"%{product_name}%", size, color))

    elif size:

        cursor = conn.execute("""
            SELECT name, size, color, quantity, price
            FROM products
            WHERE name LIKE ? AND size = ?
        """, (f"%{product_name}%", size))

    elif color:
        # search by name + color only
        cursor = conn.execute("""
            SELECT name, size, color, quantity, price
            FROM products
            WHERE name LIKE ? AND color = ?
        """, (f"%{product_name}%", color))

    else:

        cursor = conn.execute("""
            SELECT name, size, color, quantity, price
            FROM products
            WHERE name LIKE ?
        """, (f"%{product_name}%",))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return f"No product found matching '{product_name}'"

    result = f"Products found for '{product_name}':\n"
    for row in rows:
        name, size, color, quantity, price = row
        availability = "In Stock" if quantity > 0 else "Out of Stock"
        result += f"- {name} | Size: {size} | Color: {color} | Price: ${price} | {availability} ({quantity} left)\n"

    return result


def get_all_products() -> str:
    conn = sqlite3.connect("store.db")
    cursor = conn.execute("""
        SELECT name, size, color, quantity, price
        FROM products
    """)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return "No products available"

    result = "All available products:\n"
    for row in rows:
        name, size, color, quantity, price = row
        availability = "In Stock" if quantity > 0 else "Out of Stock"
        result += f"- {name} | Size: {size} | Color: {color} | Price: ${price} | {availability}\n"

    return result


def place_order(
    customer_name: str,
    customer_email: str,
    product_name: str,
    size: str,
    color: str,
    quantity: int,
    price: float
) -> str:

    conn = sqlite3.connect("store.db")

    cursor = conn.execute("""
        SELECT id, quantity, price
        FROM products
        WHERE name LIKE ? AND size = ? AND color = ?
    """, (f"%{product_name}%", size, color))

    product = cursor.fetchone()

    if not product:
        conn.close()
        return f"ERROR: Product '{product_name}' in size {size} and color {color} not found"

    product_id, available_quantity, unit_price = product

    if available_quantity < quantity:
        conn.close()
        return f"ERROR: Only {available_quantity} pieces available, customer requested {quantity}"

    total_price = unit_price * quantity

    conn.execute("""
        INSERT INTO orders
        (customer_name, customer_email, product_id, quantity, total_price, status, date)
        VALUES (?, ?, ?, ?, ?, 'confirmed', ?)
    """, (customer_name, customer_email, product_id, quantity, total_price, datetime.now().isoformat()))

    conn.execute("""
        UPDATE products
        SET quantity = quantity - ?
        WHERE id = ?
    """, (quantity, product_id))

    conn.commit()
    conn.close()

    return f"Order confirmed! {quantity}x {product_name} (Size: {size}, Color: {color}) for {customer_name}. Total: ${total_price:.2f}"


def notify_manager(message: str, customer_email: str) -> str:
    """Save a notification for the manager in the database."""
    conn = sqlite3.connect("store.db")

    conn.execute("""
        INSERT INTO notifications
        (type, message, email, timestamp, status)
        VALUES ('NEED_HUMAN', ?, ?, ?, 'unread')
    """, (message, customer_email, datetime.now().isoformat()))

    conn.commit()
    conn.close()

    return "Manager has been notified"