import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()

DATABASE_NAME = os.getenv("DATABASE_NAME")

def reporting() -> None:
    """Display the number of records loaded into each SQLite table."""
    
    with sqlite3.connect(DATABASE_NAME) as conn:
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*) FROM products")
        products = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM customers")
        customers = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM orders")
        orders = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM payments")
        payments = cur.fetchone()[0]
        
        
        print(f"Product loaded: {products}")
        print(f"Customers loaded: {customers}")
        print(f"Orders loaded: {orders}")
        print(f"Payments loaded: {payments}")
    

