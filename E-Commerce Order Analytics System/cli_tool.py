import sqlite3
from datetime import datetime, timedelta

def run_report():
    print("\nE-Commerce Reporting Tool")
    
    # 1. Take user input for report type and date range
    report_type = input("Enter report type (daily/weekly/monthly): ").strip().lower()
    start_date = input("Enter start date (YYYY-MM-DD): ").strip()
    end_date = input("Enter end date (YYYY-MM-DD): ").strip()
    
    # 2. Connect to the database
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    # 3. sql for total orders, revenue, and unique customers
    query_metrics = """
    select count(distinct o.order_id) as total_orders, sum(oi.quantity * oi.unit_price * (1 - cast(oi.discount_percent as float)/100)) as total_rev, count(distinct o.customer_id) as total_cust
    from orders as o
    join order_items as oi on o.order_id = oi.order_id
    where date(o.order_date) between ? and ?
    """
    
    # Runing query using user's dates
    cursor.execute(query_metrics, (start_date, end_date))
    metrics_result = cursor.fetchone()
    
    total_orders = metrics_result[0]
    current_revenue = metrics_result[1]
    total_customers = metrics_result[2]
    
    # If no sales, set revenue to 0
    if current_revenue is None:
        current_revenue = 0.0

    # 4.(sql)top 3 Products
    query_top_products = """
    select p.product_name, sum(oi.quantity * oi.unit_price * (1 - cast(oi.discount_percent as float)/100)) as product_rev
    from orders as o
    join order_items as oi on o.order_id = oi.order_id
    join products as p on oi.product_id = p.product_id
    where date(o.order_date) between ? and ?
    group by p.product_name
    order by product_rev desc
    limit 3
    """
    
    cursor.execute(query_top_products, (start_date, end_date))
    top_products = cursor.fetchall()
    
    # 5. Calculating previous period
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d')
    days_difference = (end_dt - start_dt).days + 1
    
    prev_end_dt = start_dt - timedelta(days=1)
    prev_start_dt = prev_end_dt - timedelta(days=days_difference - 1)
    
    # Converting dates back to strings for SQL
    prev_start_str = prev_start_dt.strftime('%Y-%m-%d')
    prev_end_str = prev_end_dt.strftime('%Y-%m-%d')
    
    cursor.execute(query_metrics, (prev_start_str, prev_end_str))
    prev_metrics_result = cursor.fetchone()
    prev_revenue = prev_metrics_result[1]
    
    if prev_revenue is None:
        prev_revenue = 0.0
        
    # calculateing percentage change
    if prev_revenue > 0:
        percent_change = ((current_revenue - prev_revenue) / prev_revenue) * 100
    else:
        percent_change = 0.0
    
    # 6. Printing Final Report
    print("\n==================================")
    print(f"SUMMARY REPORT ({report_type.upper()})")
    print(f"Date range: {start_date} to {end_date}")
    print("==================================")
    print(f"Total orders:   {total_orders}")
    print(f"Total revenue:   ${round(current_revenue, 2)}")
    print(f"Unique customers:  {total_customers}")
    print("----------------------------------")
    print("Top 3 products:")
    for product in top_products:
        print(f"- {product[0]}: ${round(product[1], 2)}")
    print("----------------------------------")
    print(f"rrevenue vs previous period: {round(percent_change, 2)}%")
    print("\n")
    
    conn.close()

if __name__ == "__main__":
    run_report()