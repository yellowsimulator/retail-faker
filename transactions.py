import uuid
from random import choice, randint
from datetime import datetime, timedelta
import pandas as pd
from products import generate_products_for_category


def generate_transactions(products: list, num_transactions: int):
    """Generate a list of transactions for customers.

    Parameters
    ----------
        products : a list of product as a dictionaries
        num_transactions : the number of transactions to generate

    Returns
    -------
        a list of transactions as dictionaries
    """
    transactions = []

    for _ in range(num_transactions):
        product = choice(products)
        transaction_id = str(uuid.uuid4())
        timestamp = datetime.now() - timedelta(days=randint(0, 365))
        quantity = randint(1, 10)

        transaction = {
            'transaction_id': transaction_id,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'product_id': product['id'],
            'product_name': product['product_name'],
            'quantity': quantity,
            'price': product['price'],
            'currency': product['currency'],
            'total': round(quantity * product['price'], 2)
        }

        transactions.append(transaction)

    return transactions


def save_transactions_to_parquet(products: list, file_path: str) -> None:
    """Save products to a parquet file

    Parameters
    ----------
        products : a list of product as a dictionaries
        file_path : the path to the parquet file to save the products to
    """
    df = pd.DataFrame(products)
    columns = ['price', 'currency', 'total', 'product_id', 'quantity', 'product_name']
    print(df[columns].head())
    exit()
    df.to_parquet(file_path)


# Example usage:
num_transactions = 100
country_name = 'United States'
category = 'Grocery & Gourmet Foods'
num_products = 10
products = generate_products_for_category(country_name, category, num_products)
transactions = generate_transactions(products, num_transactions)

save_transactions_to_parquet(transactions, 'transactions.parquet')
