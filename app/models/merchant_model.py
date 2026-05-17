import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_all_merchants():
    conn = get_db_connection()
    merchants = conn.execute('SELECT * FROM merchant ORDER BY name').fetchall()
    conn.close()
    return merchants

def get_merchant_by_id(merchant_id):
    conn = get_db_connection()
    merchant = conn.execute('SELECT * FROM merchant WHERE id = ?', (merchant_id,)).fetchone()
    conn.close()
    return merchant

def create_merchant(name, address, contact):
    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO merchant (name, address, contact) VALUES (?, ?, ?)',
        (name, address, contact)
    )
    conn.commit()
    conn.close()
    return cursor.lastrowid
