from fastapi import FastAPI
from app.api_calling import (
    fetch_products, fetch_transactions, fetch_users, enrich_transactions_with_users,
    calculate_total_spending, get_most_popular_category
)

app = FastAPI()

# Global variables to store fetched data
global products, users, transactions
products = fetch_products()  
users = fetch_users() 
transactions = fetch_transactions() 

# Enrich transactions by linking them with user details
enriched_data_users = enrich_transactions_with_users(transactions, users)

# Get category insights from enriched transaction data
category_data = get_most_popular_category(enriched_data_users)

# Endpoint to retrieve stored data for a given entity type
@app.get("/data/{entity_type}")
def get_data(entity_type: str):
    """
    Fetch stored data based on entity type.

    Args:
    entity_type (str): Type of entity ("product", "user", "transaction").

    Returns:
    dict: Corresponding entity data or an error message if the entity type is invalid.
    """
    if entity_type == "product":
        return products
    elif entity_type == "user":
        return users
    elif entity_type == "transaction":
        return transactions
    return {"error": "Invalid entity type"}

# Endpoint to analyze and return user spending insights
@app.get("/insights/users")
def get_user_insights():
    """
    Calculate and return total spending per user.

    Returns:
    dict: User spending data in the format {user_phone: total_spent}.
    """
    return {"user_spending": calculate_total_spending(enriched_data_users)}

# Endpoint to identify the most popular product category
@app.get("/insights/products")
def get_product_insights():
    """
    Determine the most popular product category based on transactions.

    Returns:
    dict: Contains the most popular category, its purchase count, and full category data.
    """
    # Refresh users and transactions to ensure up-to-date insights
    users = fetch_users()
    transactions = fetch_transactions()

    # Enrich transactions with user details for analysis
    enriched_data_users = enrich_transactions_with_users(transactions, users)
    
    # Get category purchase data
    category_data = get_most_popular_category(enriched_data_users)

    if category_data:
        most_popular_category = max(category_data, key=category_data.get)
        return {
            "most_popular_category": most_popular_category,
            "purchase_count": category_data[most_popular_category],
            "category_data": category_data 
        }

    return {
        "most_popular_category": None,
        "purchase_count": 0,
        "category_data": {} 
    }

# Run the FastAPI application when executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
