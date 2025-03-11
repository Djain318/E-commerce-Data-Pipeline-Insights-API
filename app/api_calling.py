import requests
import uuid
from datetime import datetime, timezone
from functools import wraps
from collections import defaultdict

# Decorator to transform API response
def transform_response(entity_type, source_url):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                response = func(*args, **kwargs)
                transformed_data = []
                for item in response:
                    transformed_entry = {
                        "entity_id": f"{entity_type}-{uuid.uuid4()}",
                        "entity_type": entity_type,
                        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
                        "data": item, 
                        "metadata": {
                            "source": source_url,
                            "processed_at": datetime.now(tz=timezone.utc).isoformat()
                        }
                    }
                    transformed_data.append(transformed_entry)
                return transformed_data
            except Exception as e:
                print(f"Error processing {entity_type}: {e}")
                return []
        return wrapper
    return decorator

# Apply the decorator to fetch_products
@transform_response(entity_type="product", source_url="https://fakestoreapi.com/products")
def fetch_products():
    url = "https://fakestoreapi.com/products"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Apply the decorator to fetch_transactions
@transform_response(entity_type="transaction", source_url="https://my.api.mockaroo.com/orders.json?key=e49e6840")
def fetch_transactions():
    url = "https://my.api.mockaroo.com/orders.json?key=e49e6840"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Apply the decorator to fetch_users
@transform_response(entity_type="user", source_url="https://randomuser.me/api/?results=20")
def fetch_users():
    url = "https://randomuser.me/api/?results=20"
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get("results", [])

# Enriches transaction data with product details based on matching parcel_id
def enrich_transactions_with_products(transactions, products):
    # Create a lookup dictionary for products using product ID as key
    product_lookup = {str(product["data"]["id"]): product["data"] for product in products}

    for transaction in transactions:
        parcel_id = str(transaction["data"].get("parcel_id")) 
        product_details = product_lookup.get(parcel_id, {})

        transaction["data"]["product_details"] = product_details

    return transactions

# Enriches transaction data with user details based on matching phone number
def enrich_transactions_with_users(transactions, users):
    # Create a lookup dictionary for users using phone number as key
    user_lookup = {user["data"]["phone"]: user["data"] for user in users}

    for transaction in transactions:
        user_phone = transaction["data"].get("user_phone") 
        user_details = user_lookup.get(user_phone, {}) 

        transaction["data"]["user_details"] = user_details

    return transactions

# Calculates the total spending per user based on transaction data
def calculate_total_spending(final_transactions):
    # Dictionary to accumulate total spending by user phone number
    user_spending = defaultdict(float)

    for transaction in final_transactions:
        user_phone = transaction["data"].get("user_phone") 
        product_price = transaction["data"].get("product_details", {}).get("price", 0) 
        user_spending[user_phone] += product_price  

    return dict(user_spending)

# Gets the most popular product category by counting purchases
def get_most_popular_category(final_transactions):
    # Dictionary to store category purchase count
    category_count = defaultdict(int) 

    for transaction in final_transactions:
        # Retrieve the category from product details in each transaction
        category = transaction["data"].get("product_details", {}).get("category") 
        if category:
            category_count[category] += 1 
    
    return category_count
    
# Calculates the average value of transactions based on product prices
def calculate_average_transaction_value(transactions):
    # Initialize variables for total spending and transaction count
    total_spending = 0
    total_transactions = len(transactions)

    for transaction in transactions:
        # Get product price from the transaction's product details
        product_details = transaction["data"].get("product_details", {})
        product_price = product_details.get("price", 0) 
        
        total_spending += product_price 

    average_value = total_spending / total_transactions if total_transactions > 0 else 0

    return average_value

if __name__ == "__main__":
    products = fetch_products()
    users = fetch_users()
    transactions = fetch_transactions()

    enriched_data_products = enrich_transactions_with_products(transactions, products)
    print("Here is your enriched data", enriched_data_products)
    enriched_data_users = enrich_transactions_with_users(transactions, users)
    print("Here is your enriched data", enriched_data_users)

    total_spending = calculate_total_spending(enriched_data_users)
    print("Total spending per user:", total_spending)

    category_data = get_most_popular_category(enriched_data_users)
    if category_data:
        most_popular_category = max(category_data, key=category_data.get)
        print({"most_popular_category": most_popular_category, "purchase_count": category_data[most_popular_category]})
    else:
        print({"most_popular_category": None, "purchase_count": 0})
    
    average_transaction_value = calculate_average_transaction_value(enriched_data_users)
    print(f"Average transaction value: {average_transaction_value}")
