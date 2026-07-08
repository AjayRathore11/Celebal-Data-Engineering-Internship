import sqlite3
import pandas as pd

def setup_database():
    print("Building Database\n")

    conn=sqlite3.connect('ecommerce.db')
    
    # 2. Loading csv datasets
    customers_df = pd.read_csv('data/raw_data/customers.csv')
    products_df = pd.read_csv('data/cleaned_data/cleaned_products.csv')
    orders_df = pd.read_csv('data/cleaned_data/cleaned_orders.csv')
    order_items_df = pd.read_csv('data/cleaned_data/cleaned_order_items.csv')
    
    # 3. Pushing the df's into SQLite as sql tables
    customers_df.to_sql('customers',conn,if_exists='replace',index=False)
    products_df.to_sql('products',conn,if_exists='replace',index=False)
    orders_df.to_sql('orders',conn,if_exists='replace',index=False)
    order_items_df.to_sql('order_items',conn,if_exists='replace',index=False)
    
    print("all tables are loaded into 'ecommerce.db'!\n")
    return conn
def basic_queries(conn):
    print("--- RUNNING BASIC SQL QUERIES ---\n")
    
    # Query 1: Total revenue per category
    query_1 = """
    select p.category,round(sum(oi.quantity*oi.unit_price*(1 - cast(oi.discount_percent as float)/100)), 2) as total_revenue
    from order_items as oi
    join products as p
    on oi.product_id = p.product_id
    group by p.category
    order by total_revenue desc;
    """
    print("1. Total revenue per category:")
    print(pd.read_sql_query(query_1,conn), "\n")
    
    # Query 2: Top 10 customers by total order value
    query_2 = """
    select c.customer_id, c.customer_name,round(sum(oi.quantity * oi.unit_price * (1 - cast(oi.discount_percent as float)/100)), 2) as total_order_value
    from customers c
    join orders as o on c.customer_id = o.customer_id
    join order_items as oi on o.order_id = oi.order_id
    group by c.customer_id, c.customer_name
    order by total_order_value desc
    limit 10;
    """
    print("2. Top 10 Customers by Total Order Value:")
    print(pd.read_sql_query(query_2, conn), "\n")
    
    # Query 3: Month-wise order count for the last 12 months
    query_3 = """
    select strftime('%Y-%m', order_date) as order_month,count(distinct order_id) as total_orders
    from orders
    group by order_month
    order by order_month desc
    limit 12;
    """
    print("3. Month wise oder count (last 12 months):")
    print(pd.read_sql_query(query_3,conn),"\n")

def run_intermediate_queries(conn):

    print("running intermediate     queries \n")
    
    # Query 4: Find customers who placed orders but never had any item delivered
    query_4 = """
    select distinct c.customer_id,c.customer_name
    from customers c
    join orders as o on c.customer_id = o.customer_id
    where c.customer_id not in (
        select customer_id from orders
        where status='delivered'
    );
    """
    print("4. customers with orders but No Deliveries:")
    print(pd.read_sql_query(query_4,conn), "\n")
    
    # Query 5: Products that were ordered but had more returns than purchases
    query_5 = """
    select p.product_id,p.product_name,
        sum(case when oi.quantity < 0 then abs(oi.quantity) else 0 end) as total_returned,
        sum(case when oi.quantity > 0 then oi.quantity else 0 end) as total_purchased
    from order_items as oi
    join products as p on oi.product_id =p.product_id
    group by p.product_id, p.product_name
    having total_returned>total_purchased;
    """
    print("5. Products with More Returns Than Purchases:")
    print(pd.read_sql_query(query_5,conn), "\n")
    
    # Query 6: Calculate the return rate (returned items / total items) per category
    
    query_6 = """
    select p.category,
        round(
            cast(sum(case when oi.quantity < 0 then abs(oi.quantity) else 0 end) as float) / 
            cast(sum(abs(oi.quantity)) as float) * 100, 
        2) as return_rate_percent
    from order_items oi
    join products p on oi.product_id = p.product_id
    group by p.category
    order by return_rate_percent desc;
    """
    print("6. Return Rate Per Category (%):")
    print(pd.read_sql_query(query_6, conn), "\n")

def run_advanced_queries_pt1(conn):
    print("advanced queries part 1\n")
    
    # Query 7: Running Totals with Window Functions
    query_7 = """
    with daily_region_revenue as (
        select o.region_code, date(o.order_date) as order_date, round(sum(oi.quantity * oi.unit_price * (1 - cast(oi.discount_percent as float)/100)), 2) as daily_revenue
        from orders as o
        join order_items as oi on o.order_id = oi.order_id
        group by o.region_code, date(o.order_date)
    )
    select region_code, order_date, daily_revenue, round(sum(daily_revenue) over (partition by region_code order by order_date), 2) as running_total
    from daily_region_revenue
    order by region_code,order_date;
    """
    print("7. Running totals:")
    print(pd.read_sql_query(query_7,conn).head(15),"\n") 
    
    # Query 8: Ranking with DENSE_RANK
    query_8 = """
    with product_revenue as (
        select p.category, p.product_name, round(sum(oi.quantity * oi.unit_price * (1 - cast(oi.discount_percent as float)/100)), 2) as total_revenue
        from order_items as oi
        join products as p on oi.product_id = p.product_id
        group by p.category, p.product_name
    )
    select category,product_name,total_revenue,dense_rank() over (partition by category order by total_revenue desc) as rank_in_category
    from product_revenue
    order by category, rank_in_category;
    """
    print("8. Product Revenue Rank by Category:")
    print(pd.read_sql_query(query_8, conn).head(15), "\n")
    
    # Query 9: LAG/LEAD Analysis
    query_9 = """
    with order_gaps as (
        select customer_id, date(order_date) as order_date, lag(date(order_date)) over (partition by customer_id order by order_date) as previous_order_date, julianday(date(order_date)) - julianday(lag(date(order_date)) over (partition by customer_id order by order_date)) as days_gap
        from orders
    ),
    customer_avg_gap as (
        select customer_id, avg(days_gap) as avg_gap
        from order_gaps
        group by customer_id
    )
    select og.customer_id,og.order_date, og.previous_order_date,og.days_gap, 
        case 
            when cag.avg_gap > 30 then 'at risk' 
            else 'safe' end as risk_flag
    from order_gaps as og
    join customer_avg_gap as cag on og.customer_id = cag.customer_id
    where og.previous_order_date is not null
    order by og.customer_id,og.order_date;
    """
    print("9.Analysis")
    print(pd.read_sql_query(query_9,conn).head(15), "\n")
    
    # Query 10: CTE with Multiple Levels
    query_10 = """
    with monthly_customer_revenue as (
        select o.customer_id, strftime('%Y-%m', o.order_date) as order_month, sum(oi.quantity * oi.unit_price * (1 - cast(oi.discount_percent as float)/100)) as monthly_revenue
        from orders as o
        join order_items as oi on o.order_id = oi.order_id
        group by o.customer_id, strftime('%Y-%m', o.order_date)
    ),
    categorized_customers as (
        select order_month, customer_id, case when monthly_revenue > 10000 then 'high' when monthly_revenue between 5000 and 10000 then 'medium' else 'low' end as revenue_category
        from monthly_customer_revenue
    )
    select order_month,revenue_category,count(customer_id) as customer_count
    from categorized_customers
    group by order_month,revenue_category
    order by order_month desc,revenue_category;
    """
    print("10. count of customers in each category per month:")
    print(pd.read_sql_query(query_10, conn).head(15), "\n")
    
    # Query 11: NTILE for Segmentation
    query_11 = """
    with lifetime_value as (
        select o.customer_id, round(sum(oi.quantity * oi.unit_price * (1 - cast(oi.discount_percent as float)/100)), 2) as total_value
        from orders as o
        join order_items as oi on o.order_id = oi.order_id
        group by o.customer_id
    ),
    quartiles as (
        select customer_id,total_value,ntile(4) over (order by total_value desc) as quartile
        from lifetime_value
    )
    select customer_id, total_value, quartile, 
        case 
            when quartile = 1 then 'platinum' 
            when quartile = 2 then 'gold' when quartile = 3 then 'silver' 
            else 'bronze' end as quartile_label
    from quartiles
    order by quartile,total_value desc;
    """
    print("11. NTILE Customer Lifetime Value Segmentation:")
    print(pd.read_sql_query(query_11, conn).head(15), "\n")

def run_advanced_queries_pt2(conn):
    print("advanced_queries (PT 2)\n")
    
    # Query 12: Year-over-Year Comparison
    
    query_12 = """
    with monthly_revenue as (
        select strftime('%Y', o.order_date) as year, strftime('%m', o.order_date) as month, round(sum(oi.quantity * oi.unit_price * (1 - cast(oi.discount_percent as float)/100)), 2) as revenue
        from orders as o
        join order_items as oi on o.order_id = oi.order_id
        group by strftime('%Y', o.order_date), strftime('%m', o.order_date)
    )
    select curr.year, curr.month, curr.revenue, coalesce(prev.revenue, 0) as prev_year_revenue, case when prev.revenue is null then null else round(((curr.revenue - prev.revenue) / prev.revenue) * 100, 2) end as yoy_growth_percent
    from monthly_revenue as curr
    left join monthly_revenue as prev on cast(curr.year as integer) - 1 = cast(prev.year as integer) and curr.month = prev.month
    order by curr.year desc, curr.month desc;
    """
    print("12. Year-over-Year Comparison:")
    print(pd.read_sql_query(query_12, conn).head(15), "\n")
    
    # Query 13: First/Last Value Analysis
    query_13 = """
    with customer_purchases as (
        select o.customer_id, p.category, o.order_date, first_value(p.category) over (partition by o.customer_id order by o.order_date) as first_category, last_value(p.category) over (partition by o.customer_id order by o.order_date range between unbounded preceding and unbounded following) as last_category
        from orders as o
        join order_items as oi on o.order_id = oi.order_id
        join products as p on oi.product_id = p.product_id
    ),
    customer_shift as (
        select distinct customer_id, first_category, last_category
        from customer_purchases
    )
    select customer_id, first_category, last_category, case when first_category != last_category then 'yes' else 'no' end as category_shift
    from customer_shift
    order by customer_id;
    """
    print("13. First vs Last Purchased Category:")
    print(pd.read_sql_query(query_13, conn).head(15), "\n")
    
    # Query 14: Cumulative Distribution
    query_14 = """
    with customer_revenue as (
        select o.customer_id, round(sum(oi.quantity * oi.unit_price * (1 - cast(oi.discount_percent as float)/100)), 2) as revenue
        from orders as o
        join order_items as oi on o.order_id = oi.order_id
        group by o.customer_id
    ),
    total_calc as (
        select sum(revenue) as total_revenue
        from customer_revenue
    ),
    running_calc as (
        select cr.customer_id, cr.revenue, sum(cr.revenue) over (order by cr.revenue desc) as cumulative_revenue
        from customer_revenue as cr
    )
    select rc.customer_id, rc.revenue, rc.cumulative_revenue, round((rc.cumulative_revenue / tc.total_revenue) * 100, 2) as cumulative_percent
    from running_calc as rc
    cross join total_calc as tc
    order by rc.revenue desc;
    """
    print("14. Cumulative Revenue Distribution:")
    print(pd.read_sql_query(query_14, conn).head(15), "\n")
    
    # Query 15: Cohort Analysis
    query_15 = """
    with cohorts as (
        select customer_id, strftime('%Y-%m', registration_date) as cohort_month
        from customers
    ),
    order_months as (
        select o.customer_id, (cast(strftime('%Y', o.order_date) as integer) - cast(strftime('%Y', c.registration_date) as integer)) * 12 + (cast(strftime('%m', o.order_date) as integer) - cast(strftime('%m', c.registration_date) as integer)) as month_index
        from orders as o
        join customers as c on o.customer_id = c.customer_id
    ),
    cohort_sizes as (
        select cohort_month, count(distinct customer_id) as total_customers
        from cohorts
        group by cohort_month
    ),
    retention_counts as (
        select c.cohort_month, om.month_index, count(distinct om.customer_id) as active_customers
        from cohorts as c
        left join order_months as om on c.customer_id = om.customer_id
        where om.month_index between 0 and 3
        group by c.cohort_month, om.month_index
    )
    select cs.cohort_month, max(case when rc.month_index = 0 then rc.active_customers else 0 end) as month_0_orders, max(case when rc.month_index = 1 then rc.active_customers else 0 end) as month_1_orders, max(case when rc.month_index = 2 then rc.active_customers else 0 end) as month_2_orders, max(case when rc.month_index = 3 then rc.active_customers else 0 end) as month_3_orders, round(cast(max(case when rc.month_index = 0 then rc.active_customers else 0 end) as float) / cs.total_customers * 100, 2) as retention_month_0, round(cast(max(case when rc.month_index = 1 then rc.active_customers else 0 end) as float) / cs.total_customers * 100, 2) as retention_month_1, round(cast(max(case when rc.month_index = 2 then rc.active_customers else 0 end) as float) / cs.total_customers * 100, 2) as retention_month_2, round(cast(max(case when rc.month_index = 3 then rc.active_customers else 0 end) as float) / cs.total_customers * 100, 2) as retention_month_3
    from cohort_sizes as cs
    left join retention_counts as rc on cs.cohort_month = rc.cohort_month
    group by cs.cohort_month, cs.total_customers
    order by cs.cohort_month desc;
    """
    print("15. Cohort Retention Analysis (Months 0-3):")
    print(pd.read_sql_query(query_15, conn).head(15), "\n")
    
    # Query 16: Self-Join with Window Function
    query_16 = """
    with product_pairs as (
        select a.product_id as p1, b.product_id as p2
        from order_items as a
        join order_items as b on a.order_id = b.order_id
        where a.product_id < b.product_id
    )
    select p1_info.product_name as product_a, p2_info.product_name as product_b, count(*) as times_bought_together
    from product_pairs as pp
    join products as p1_info on pp.p1 = p1_info.product_id
    join products as p2_info on pp.p2 = p2_info.product_id
    group by p1_info.product_name, p2_info.product_name
    order by times_bought_together desc
    limit 15;
    """
    print("16. frequently bought together products:")
    print(pd.read_sql_query(query_16,conn),"\n")

# --- Execution ---
if __name__ == "__main__":
    db_connection = setup_database()
    basic_queries(db_connection)
    run_intermediate_queries(db_connection)
    run_advanced_queries_pt1(db_connection)
    run_advanced_queries_pt2(db_connection) 
    db_connection.close()
    print("PART 3: SQL ANALYSIS COMPLETE ")

