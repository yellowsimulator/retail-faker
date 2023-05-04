
import random
import pyarrow as pa
import pandas as pd
from tqdm import tqdm
from faker import Faker
from pathlib import Path
import multiprocessing as mp
import pyarrow.parquet as pq
from countryinfo import CountryInfo
from forex_python.converter import CurrencyRates
from forex_python.bitcoin import BtcConverter

fake = Faker()

from helper_functions import load_subcategories_from_yaml
from helper_functions import load_categories_from_yaml
from helper_functions import get_currency_code
from helper_functions import get_inflation_rate
from helper_functions import get_currency_code
from helper_functions import get_currency_code
from helper_functions import get_exchange_rate


def save_product_data(product_df: pd.DataFrame) -> None:
    """Creates a folder `retail_data` if it doesn't exist.
       Then saves the data in the folder as in :
       retail_data/`products.parquet`.

    Parameters
    ----------
        product_df: the product data as a pandas DataFrame

    Returns
    -------
        None
    """
    folder_path = Path('retail_data')
    if not folder_path.exists():
        folder_path.mkdir()
    table = pa.Table.from_pandas(product_df)
    file_path = folder_path / 'products.parquet'
    pq.write_table(table, file_path)


def get_country_data(country_name: str) -> tuple:
    """Returns the contry data after handling the exceptions.

    Parameters
    ----------
        country_name: the name of the country

    Returns
    -------
        a tuple of (currency_code, inflation, exchange_rate)
    """
    try:
        currency_code = get_currency_code(country_name)
        inflation = get_inflation_rate(country_name)
        exchange_rate = get_exchange_rate(country_name)
    except:
        print(f'No data for {country_name}!. Using United States data instead.')
        country_name = 'United States'
        currency_code = get_currency_code(country_name)
        inflation = get_inflation_rate(country_name)
        exchange_rate = get_exchange_rate(country_name)

    return currency_code, inflation, exchange_rate



def generate_a_row_product_data(args):
    """Genrates a single product data row.
    """
    _, categories, currency_code, inflation, exchange_rate = args
    category = random.choice(categories)
    subcategories_dict = load_subcategories_from_yaml(category)
    subcategories = list(subcategories_dict.keys())
    subcategory = random.choice(subcategories)
    prices = subcategories_dict[subcategory]
    return {
        'product_id': fake.uuid4(),
        'product_name': fake.bs().title(),
        'description': fake.sentence(),
        'category': category,
        'subcategory': subcategory,
        'brand': fake.company(),
        'price_in_usd': round(random.uniform(prices[0], prices[0]), 2),
        'inflation_rate': inflation,
        'exchange_rate': exchange_rate,
        'currency': currency_code,
        'expiration_date': fake.date_between(start_date='+30d', end_date='+365d').strftime('%Y-%m-%d'),
    }


def generate_random_product_data(country_name: str, numb_products: int,
                                 is_saved: bool = False):
    """Generates random store data for a given country.

    Parameters
    ----------
        country_name: the country to generate store data for
        numb_stores: the number of stores to generate
        is_saved: whether to save the generated data or not.
                  if True, the data will be saved in the current directory
                  with the name `products.parquet`

    Returns
    -------
        stores: the generated stores
    """
    categories = load_categories_from_yaml()
    currency_code, inflation, exchange_rate = get_country_data(country_name)
    numb = f'{numb_products:,}'.replace(',', ' ')

    with mp.Pool(mp.cpu_count()) as pool:
        products = list(tqdm(pool.imap(generate_a_row_product_data,
                                        [(i, categories, currency_code, inflation, exchange_rate)
                                         for i in range(numb_products)]),
                             total=numb_products, desc=f'Generating {numb} products data!'))
    product_df = pd.DataFrame(products)

    if is_saved:
        save_product_data(product_df)
    return product_df


if __name__ == '__main__':
    ...
