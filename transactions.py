import uuid
import random
import pandas as pd
from tqdm import tqdm
from faker import Faker
import pyarrow as pa
from pathlib import Path
import pyarrow.parquet as pq
from datetime import datetime, timedelta
from products import generate_random_product_data
fake = Faker()


def generate_random_transaction_data(num_transactions: int,
                                     numb_unique_ids: int,
                                     is_saved: bool = False):
    """Generate a list of transactions for customers.

    Parameters
    ----------
        products : a list of product as a dictionaries
        num_transactions : the number of transactions to generate

    Returns
    -------
        a list of transactions as dictionaries
    """
    file_path = Path('retail_data/products.parquet')
    products = pd.read_parquet(file_path)
    m = len(products)
    transactions = []
    numb = f'{num_transactions:,}'.replace(',', ' ')
    unique_ids = [str(uuid.uuid4()) for _ in range(numb_unique_ids)]
    for k in tqdm(range(num_transactions), desc=f"Generating {numb} transactions"):
        transaction_id = random.choice(unique_ids)
        timestamp = datetime.now() - timedelta(days=random.randint(0, 365))
        quantity = random.randint(1, 30)
        random_product_row = products.sample(n=1)
        #print(random_product_row.iloc[0]['price_in_usd'])
        try:
            price = (random_product_row.iloc[0]['price_in_usd'])/(random_product_row.iloc[0]['exchange_rate'])
            total = round(quantity * random_product_row.iloc[0]['price_in_usd']/random_product_row.iloc[0]['exchange_rate'], 2)
            currency = random_product_row.iloc[0]['currency']
            exchange_rate = random_product_row.iloc[0]['exchange_rate']
        except TypeError:
            price = random_product_row.iloc[0]['price_in_usd']
            exchange_rate = None
            total = round(quantity * random_product_row.iloc[0]['price_in_usd'], 2)
            currency = 'USD'
        transaction = {
            'transaction_id': transaction_id,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'product_id': random_product_row.iloc[0]['product_id'],
            'product_name': random_product_row.iloc[0]['product_name'],
            'quantity': quantity,
            'price': price,
            'exchange_rate': exchange_rate,
            'currency': currency,
            'inflation_rate': random_product_row.iloc[0]['inflation_rate'],
            'total': total
        }
        transactions.append(transaction)

    df_transactions = pd.DataFrame(transactions)
    if is_saved:
        folder_path = Path('retail_data')
        table = pa.Table.from_pandas(df_transactions)
        file_path = folder_path / 'transactions.parquet'
        pq.write_table(table, file_path)
        return None
    return df_transactions



if __name__ == "__main__":
    generate_random_transaction_data(10, is_saved=True)


