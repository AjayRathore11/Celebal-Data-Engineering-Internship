import pandas as pd

def edge_case_tests():
    print("RUNNING EDGE CASE TESTS\n")
    
    # 1. Loading data
    orders = pd.read_csv('data/raw_data/orders.csv')
    items = pd.read_csv('data/raw_data/order_items.csv')
    
    # Test 1: What happens when an item has an order_id not in orders?
    
    print("Test 1: checking for items with no matching order")
    valid_order_ids = orders['order_id'].unique()
    lost_items = items[~items['order_id'].isin(valid_order_ids)]
    if len(lost_items) > 0:
        print(f" Alert :founded {len(lost_items)} items that don't belong to  real order!")
    else:
        print(" Pass: all items match real order.")

    # Test 2: What happens when discount_percent > 100?
    print("\nTest 2: checking for discounts(above 100%)")
    high_discounts = items[items['discount_percent'] > 100]
    
    if len(high_discounts) > 0:
        print(f"Alert: found {len(high_discounts)} items where the company is paying the customer!")
    else:
        print(" Pass: No discounts are over 100%.")

    # Test 3: What happens when quantity is 0?
    
    print("\nTest 3: Check items with 0 quantity")
    zero_quantity = items[items['quantity'] == 0]
    
    if len(zero_quantity) > 0:
        print(f"Alert: Found {len(zero_quantity)} items with 0 quantity!")
    else:
        print("passs : No one tried to buy 0 items.")

    # Test 4: What happens when order_date is in the future?
   
    print("\nTest 4: Checkingfor orders from the future")
    
    orders['order_date'] = pd.to_datetime(orders['order_date'], format='mixed', errors='coerce')
    
    right_now = pd.to_datetime('today')
    
    # Checking for future dates
    future_orders = orders[orders['order_date'] > right_now]
    
    if len(future_orders) > 0:
        print(f"Alert: Found {len(future_orders)} orders in the future!")
    else:
        print("pass: All orders happened in the past or present.")
        
    print("\nall tests are now complete")


if __name__ == "__main__":
    edge_case_tests()