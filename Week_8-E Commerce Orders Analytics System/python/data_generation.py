import csv
import random
from datetime import datetime, timedelta

# --- Configuration ---
NUM_CUSTOMERS = 500
NUM_PRODUCTS = 50
NUM_ORDERS = 800
NUM_ORDER_ITEMS = 2000

# --- Helper Functions ---
def random_date(start_year=2022):
    start = datetime(start_year, 1, 1)
    end = datetime.now()
    return start + timedelta(days=random.randint(0, (end - start).days))

# --- 1. Generate Customers ---
def generate_customers():
    print("Generating customers.csv")
    customer_types = ['REGULAR', 'PREMIUM', 'VIP']
    
    # Updated to Indian names
    first_names = ['Rahul', 'Amit', 'Priya', 'Neha', 'Arjun', 'Anjali', 'Vikram', 'Sneha', 'Rohan', 'Kavya']
    last_names = ['Sharma', 'Patel', 'Singh', 'Kumar', 'Gupta', 'Verma', 'Joshi', 'Reddy', 'Das', 'Yadav']
    
    with open('data/raw_data/customers.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['customer_id', 'customer_name', 'email', 'registration_date', 'customer_type'])
        
        for i in range(1, NUM_CUSTOMERS + 1):
            name = f"{random.choice(first_names)} {random.choice(last_names)}"
            
            # Intentional Issue: 2% of emails should be invalid (missing @ or domain)
            if random.random() < 0.02:
                email = f"{name.replace(' ', '').lower()}gmail.com" # Missing @
            else:
                email = f"{name.replace(' ', '').lower()}@example.com"
                
            reg_date = random_date().strftime('%Y-%m-%d')
            c_type = random.choice(customer_types)
            
            writer.writerow([i, name, email, reg_date, c_type])

# --- 2. Generate Products ---
def generate_products():
    print("Generating products.csv...")
    categories = {
        'Electronics': ['Phones', 'Laptops', 'Audio'],
        'Clothing': ['Shirts', 'Pants', 'Shoes'],
        'Home': ['Furniture', 'Decor', 'Kitchen'],
        'Books': ['Fiction', 'Non-Fiction', 'Educational']
    }
    
    with open('data/raw_data/products.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['product_id', 'product_name', 'category', 'subcategory', 'cost_price'])
        
        for i in range(1, NUM_PRODUCTS + 1):
            category = random.choice(list(categories.keys()))
            subcategory = random.choice(categories[category])
            
            # Base product name
            product_name = f"{subcategory[:-1]} Model {random.randint(10, 99)}"
            
            # Intentional Issue: Some product names have extra spaces or mixed case
            if random.random() < 0.15:
                product_name = f"  {product_name.lower()}  "
            elif random.random() < 0.15:
                product_name = product_name.upper()
                
            cost_price = round(random.uniform(10.0, 500.0), 2)
            
            writer.writerow([i, product_name, category, subcategory, cost_price])



# --- 3. Generate Orders ---
def generate_orders():
    print("Generating orders.csv...")
    statuses = ['PLACED', 'SHIPPED', 'DELIVERED', 'CANCELLED', 'RETURNED']
    regions = ['NORTH', 'SOUTH', 'EAST', 'WEST']
    
    with open('data/raw_data/orders.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['order_id', 'customer_id', 'order_date', 'status', 'region_code'])
        
        for i in range(1, NUM_ORDERS + 1):
            # Intentional Issue: 5% of orders should have NULL customer_id
            if random.random() < 0.05:
                customer_id = "" # Leaving it empty mimics NULL in CSV
            else:
                customer_id = random.randint(1, NUM_CUSTOMERS)
            
            dt = random_date()
            # Intentional Issue: Some orders have wrong date format (DD-MM-YYYY)
            if random.random() < 0.10: # 10% chance for wrong format
                order_date = dt.strftime('%d-%m-%Y %H:%M:%S')
            else:
                order_date = dt.strftime('%Y-%m-%d %H:%M:%S')
                
            status = random.choice(statuses)
            region = random.choice(regions)
            
            writer.writerow([i, customer_id, order_date, status, region])

# --- 4. Generate Order Items ---
def generate_order_items():
    print("Generating order_items.csv")
    
    with open('data/raw_data/order_items.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['item_id', 'order_id', 'product_id', 'quantity', 'unit_price', 'discount_percent'])
        
        for i in range(1, NUM_ORDER_ITEMS + 1):
            
            if random.random() < 0.01:
                order_id = NUM_ORDERS + 9999 # This order_id will NOT exist in orders.csv
            else:
                order_id = random.randint(1, NUM_ORDERS)
                
            product_id = random.randint(1, NUM_PRODUCTS)
            
            # Intentional Issue: 3% of order_items should have negative quantity
            quantity = random.randint(1, 5)
            if random.random() < 0.03:
                quantity = -quantity
                
            unit_price = round(random.uniform(10.0, 500.0), 2)
            discount_percent = random.randint(0, 100)
            
            writer.writerow([i, order_id, product_id, quantity, unit_price, discount_percent])

# --- Execution ---
if __name__ == "__main__":
    generate_customers()
    generate_products()
    generate_orders()
    generate_order_items()
    print("All 4 CSV files generated successfully! Part 1 is complete.")