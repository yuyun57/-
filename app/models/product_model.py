import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_all_products(filters=None):
    conn = get_db_connection()
    query = 'SELECT p.*, m.name as merchant_name FROM product p JOIN merchant m ON p.merchant_id = m.id WHERE p.status != "下架"'
    params = []
    
    if filters:
        if 'max_price' in filters and filters['max_price']:
            query += ' AND p.discount_price <= ?'
            params.append(int(filters['max_price']))
        if 'type' in filters and filters['type']:
            query += ' AND p.type = ?'
            params.append(filters['type'])
        if 'merchant_id' in filters and filters['merchant_id']:
            query += ' AND p.merchant_id = ?'
            params.append(int(filters['merchant_id']))
            
    query += ' ORDER BY p.created_at DESC'
            
    products = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in products]

def get_product_by_id(product_id):
    conn = get_db_connection()
    product = conn.execute(
        'SELECT p.*, m.name as merchant_name, m.address as merchant_address '
        'FROM product p JOIN merchant m ON p.merchant_id = m.id WHERE p.id = ?', 
        (product_id,)
    ).fetchone()
    conn.close()
    return dict(product) if product else None

def create_product(merchant_id, name, type, original_price, discount_price, quantity, image_url, pickup_time):
    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO product (merchant_id, name, type, original_price, discount_price, quantity, image_url, pickup_time) '
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (merchant_id, name, type, original_price, discount_price, quantity, image_url, pickup_time)
    )
    conn.commit()
    conn.close()
    return cursor.lastrowid

def update_product(product_id, name, type, original_price, discount_price, quantity, pickup_time):
    conn = get_db_connection()
    conn.execute(
        'UPDATE product SET name = ?, type = ?, original_price = ?, discount_price = ?, quantity = ?, pickup_time = ? WHERE id = ?',
        (name, type, original_price, discount_price, quantity, pickup_time, product_id)
    )
    conn.commit()
    conn.close()

def update_product_status(product_id, status):
    conn = get_db_connection()
    conn.execute('UPDATE product SET status = ? WHERE id = ?', (status, product_id))
    conn.commit()
    conn.close()
    
def delete_product(product_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM product WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()
