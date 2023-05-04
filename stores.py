import pandas as pd
import random
import pyarrow as pa
from pathlib import Path
import pyarrow.parquet as pq
import multiprocessing as mp
from tqdm import tqdm
from faker import Faker
fake = Faker()

from helper_functions import get_regions_of_country
from helper_functions import timer_decorator

def save_store_data(stores_df: pd.DataFrame) -> None:
    """Creates a folder `retail_data` if it doesn't exist.
         Then saves the data in the folder as in :
            retail_data/`stores.parquet`.

    Parameters
    ----------
        stores_df: the stores data as a pandas DataFrame

    Returns
    -------
        None
    """
    folder_path = Path('retail_data')
    if not folder_path.exists():
        folder_path.mkdir()
    table = pa.Table.from_pandas(stores_df)
    file_path = folder_path / 'stores.parquet'
    pq.write_table(table, file_path)


def get_regions(country_name: str):
    """Handle the exceptions when getting the regions of a country.
        then returns the regions of the country.

    Parameters
    ----------
        country_name: the name of the country

    Returns
    -------
        regions: the regions of the country
    """
    try:
        regions = get_regions_of_country(country_name)
    except:
        print(f'No data for {country_name}!. Using United States data instead.')
        country_name = 'United States'
        country_name = 'United States'
        regions = [country_name]
    return regions, country_name


def generate_a_row_store_data(args):
    """Genrates a single store data row.
    """
    _, country_name, regions = args
    region_name = random.choice(regions)
    return {
        "store_id": fake.uuid4(),
        "store Name": fake.company(),
        "address": fake.street_address(),
        "city": fake.city(),
        "state_or_Province": region_name,
        "country": country_name,
        "postal/Zip Code": fake.zipcode(),
        "store_type": random.choice(["Supermarket", "Convenience Store", "Department Store"]),
        "opening_hours": "8:00 AM - 9:00 PM",
        "manager": fake.name(),
        "number_of_employees": random.randint(5, 100),
        "number_of_non_self_checkout_lanes": random.randint(2, 20),
        "number_of_self_checkout_lanes": random.randint(0, 4)
    }


def generate_random_store_data(country_name: str,
                               numb_stores: int,
                               is_saved: bool = False):
    """Generates random store data for a given country.

    Parameters
    ----------
        country_name: the country to generate store data for
        numb_stores: the number of stores to generate

    Returns
    -------
        stores: the generated stores
    """
    regions, country_name = get_regions(country_name)
    numb = f'{numb_stores:,}'.replace(',', ' ')

    with mp.Pool(mp.cpu_count()) as pool:
        args_list = [(i, country_name, regions) for i in range(numb_stores)]

        with tqdm(total=len(args_list), desc=f"Generating {numb} stores data") as pbar:
            result = []
            for store in pool.imap_unordered(generate_a_row_store_data, args_list):
                result.append(store)
                pbar.update()

    stores_df = pd.DataFrame(result)
    if is_saved:
        save_store_data(stores_df)
    return stores_df



if __name__ == "__main__":
    pd.set_option('display.max_columns', None)



