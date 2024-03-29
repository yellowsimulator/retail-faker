
from products import generate_random_product_data
from transactions import generate_random_transaction_data
from stores import generate_random_store_data



def generate_random_retail_data(country_name: str,
                                num_stores: int,
                                num_products: int,
                                num_transactions: int,
                                numb_unique_ids: int):
    """Generates random retail data for a given country.

    Parameters
    ----------
        country_name: the country to generate retail data for
        num_stores: the number of stores to generate
        num_products: the number of products to generate
        num_transactions: the number of transactions to generate

    Returns
    -------
        stores: the generated stores
        products: the generated products
        transactions: the generated transactions
    """
    generate_random_product_data(country_name, num_products, is_saved=True)
    generate_random_store_data(country_name, num_stores, is_saved=True)
    generate_random_transaction_data(num_transactions, numb_unique_ids, is_saved=True)


if __name__ == "__main__":
    import pandas as pd
    country_name = 'Denmark'
    num_stores = 100
    num_products = 10000
    num_transactions = 1000
    numb_unique_ids = 20
    generate_random_retail_data(country_name, num_stores, num_products, num_transactions, numb_unique_ids)
    df = pd.read_parquet('retail_data/transactions.parquet')
    print(df.head())

