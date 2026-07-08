import pandas as pd

#  1. Cleaning file  => products 
def clean_products():
    print("cleaning the file = > products.csv")
    df = pd.read_csv('data/raw_data/products.csv')
    df['product_name'] = df['product_name'].str.strip().str.title()
    
    # Saveing
    df.to_csv('data/cleaned_data/cleaned_products.csv', index=False)
    print("cleaned and saved to cleaned_products.csv\n")
    return df

#  2. cleaning orders 
def clean_orders():
    print("cleaning file => orders.csv")

    df = pd.read_csv('data/raw_data/orders.csv')
    null_count = df['customer_id'].isna().sum()
    print(f"Founded {null_count} orders with missing customer id's and filling with -1.")
    df['customer_id'] = df['customer_id'].fillna(-1).astype(int)
    
 
    df['order_date'] = pd.to_datetime(df['order_date'], format='mixed')
    
    # Saving
    df.to_csv('data/cleaned_data/cleaned_orders.csv', index=False)
    print("Orders file is cleaned and saved to cleaned_orders.csv\n")
    return df

#  3. validate emails 
def validate_emails():
    print("validating emails")
    df_customers =pd.read_csv('data/raw_data/customers.csv')
    

    invalid_mask = ~df_customers['email'].str.contains('@') | ~df_customers['email'].str.contains(r'\.')
    invalid_customers = df_customers[invalid_mask]
    
    bad_ids = invalid_customers['customer_id'].tolist()
    
    return bad_ids

# --- 4. Check Referential Integrity ---
def check_referential_integrity():
    print("Checking the a referential integrity")
    df_items=   pd.read_csv('data/raw_data/order_items.csv')
    df_orders= pd.read_csv('data/raw_data/orders.csv')
    
    valid_order_ids =df_orders['order_id'].unique()
    
    orphan_items= df_items[~df_items['order_id'].isin(valid_order_ids)]
    bad_order_references= orphan_items['order_id'].unique().tolist()
    
    print(f"Found {len(orphan_items)} items referencing non-existent orders.")
    print(f"invalid order ids found in order_items.csv: {bad_order_references}\n")
    
    # Saveing the cleaned order_items
    clean_items = df_items[df_items['order_id'].isin(valid_order_ids)]
    
    clean_items.to_csv('data/cleaned_data/cleaned_order_items.csv', index=False)
    print("cleaned order items saved to cleaned_order_items.csv\n")
    
    return orphan_items


if __name__ == "__main__":
    print("starting Data Cleaning Process\n")
    clean_products()
    clean_orders()
    invalid_emails = validate_emails()
    orphan_items = check_referential_integrity()

    print("Now the data CleaningG is complete")