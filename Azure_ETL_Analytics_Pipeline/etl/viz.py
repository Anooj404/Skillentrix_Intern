import os
import sqlite3

import matplotlib.pyplot as plt
from dotenv import load_dotenv
from matplotlib.ticker import MaxNLocator
from weasyprint import HTML

load_dotenv()
DATABASE_NAME = os.getenv("DATABASE_NAME")

def generate_product_sales_chart(cur) -> None:
    """Generate a bar chart showing quantity sold per product."""
    
    cur.execute("""SELECT products.product_name,
                SUM(orders.quantity) FROM orders 
                INNER JOIN products 
                ON orders.product_id = products.product_id 
                GROUP BY products.product_name""")
    product_sales = cur.fetchall()
    print(product_sales)
            
    product_name = [row[0] for row in product_sales]
    quantities = [row[1] for row in product_sales]
            
    plt.bar(product_name,quantities)
    plt.xlabel("Product Name")
    plt.ylabel("Quantity Sold")
    plt.title("Quantity Sold Per Product")
        
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.savefig("reports/product_sales.png")
    plt.close()
            
def generate_revenue_data_chart(cur) -> None:
    """Generate a pie chart showing revenue per product."""
    
    cur.execute("""SELECT products.product_name,
                SUM(orders.quantity * products.price)
                FROM orders 
                INNER JOIN products 
                ON orders.product_id = products.product_id 
                GROUP BY products.product_name""")
    revenue_data = cur.fetchall()
    revenue_products = [row[0] for row in revenue_data]
    revenues = [row[1] for row in revenue_data]
            
    plt.figure(figsize=(8, 6))
    
    plt.pie(
        revenues,
        autopct="%1.1f%%",
        pctdistance=0.75
    )
    
    plt.legend(revenue_products,
    loc="center left",
    bbox_to_anchor = (1, 0.5))
    
    plt.title("Revenue Per Product")
    
    plt.savefig("reports/product_revenue.png")
    plt.close()
    
def generate_order_over_time_chart(cur) -> None:
    """Generate a line chart showing orders over time."""
    
    cur.execute("""SELECT DATE(order_date),
                COUNT(*) FROM orders
                GROUP BY DATE(order_date)
                ORDER BY DATE(order_date)""")
    order_date = cur.fetchall()
            
    dates = [row[0] for row in order_date]
    order_count = [row[1] for row in order_date]
    plt.figure(figsize = (8, 5))
    plt.plot(dates,order_count, marker="o")
    plt.xlabel("Date")
    plt.ylabel("Number of Orders")
    plt.title("Orders over Time")
            
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xticks(rotation = 45)
    plt.tight_layout()
    plt.grid()
    plt.savefig("reports/orders_over_time.png")
    plt.close()

def generate_report(total_products: int,
                    total_customers: int,
                    total_orders:int,
                    total_revenue: float) -> None:
    """Generate the HTML and PDF analytics report."""
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    
        <meta charset="UTF-8">
    
        <title>ETL Analytics Report</title>
    
        <style>
    
            body {{
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
                margin: 0;
                padding: 30px;
            }}
    
            .container {{
                max-width: 1000px;
                margin: auto;
                background-color: white;
                padding: 30px;
                border-radius: 10px;
            }}
    
            h1 {{
                text-align: center;
            }}
    
            .summary {{
                display: flex;
                justify-content: space-between;
                gap: 15px;
            }}
    
            .card {{
                flex: 1;
                text-align: center;
                padding: 20px;
                background-color: #eeeeee;
                border-radius: 8px;
            }}
    
            .card h3 {{
                margin-bottom: 10px;
            }}
    
            .card p {{
                font-size: 22px;
                font-weight: bold;
            }}
    
            .chart {{
                text-align: center;
                margin-top: 40px;
            }}
    
            .chart img {{
                width: 700px;
                max-width: 100%;
            }}
    
        </style>
    
    </head>
    
    <body>
    
    <div class="container">
    
        <h1>ETL Analytics Report</h1>
    
        <h2>Summary</h2>
    
        <div class="summary">
    
            <div class="card">
                <h3>Products</h3>
                <p>{total_products}</p>
            </div>
    
            <div class="card">
                <h3>Customers</h3>
                <p>{total_customers}</p>
            </div>
    
            <div class="card">
                <h3>Orders</h3>
                <p>{total_orders}</p>
            </div>
    
            <div class="card">
                <h3>Total Revenue</h3>
                <p>₹{total_revenue:,.2f}</p>
            </div>
    
        </div>
    
        <div class="chart">
            <h2>Quantity Sold Per Product</h2>
            <img src="product_sales.png">
        </div>
    
        <div class="chart">
            <h2>Revenue Per Product</h2>
            <img src="product_revenue.png">
        </div>
    
        <div class="chart">
            <h2>Orders Over Time</h2>
            <img src="orders_over_time.png">
        </div>
    
    </div>
    
    </body>
    </html>
"""
    with open("reports/report.html","w") as file:
        file.write(html)
    HTML("reports/report.html").write_pdf("reports/ETL_Report.pdf")
    
def generate_visuals() -> None:
    """Generate analytics charts, an HTML report, and a PDF report."""
    
    with sqlite3.connect(DATABASE_NAME) as conn:
        cur = conn.cursor()
        
        generate_product_sales_chart(cur)
        generate_revenue_data_chart(cur)
        generate_order_over_time_chart(cur)
        
        cur.execute("""SELECT SUM(orders.quantity * products.price)
                    FROM orders 
                    INNER JOIN products 
                    ON orders.product_id = products.product_id""")
        total_revenue = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM products")
        total_products = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM customers")
        total_customers = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM orders")
        total_orders = cur.fetchone()[0]

        print("Total Products:", total_products)
        print("Total Customers:", total_customers)
        print("Total Orders:", total_orders)
        print("Total Revenue:", total_revenue)
        
        generate_report(total_products,
                        total_customers,
                        total_orders,
                        total_revenue)
        
        
        
       
            
