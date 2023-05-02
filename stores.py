import pandas as pd
import random
import string
from faker import Faker
fake = Faker()

from helper_functions import get_regions_of_country
from helper_functions import generate_random_coords_in_region



def generate_random_store_data(country_name: str, numb_stores: int):
    """Generates random store data for a given country.

    Parameters
    ----------
        country_name: the country to generate store data for
        numb_stores: the number of stores to generate

    Returns
    -------
        stores: the generated stores
    """
    stores = []
    regions = get_regions_of_country(country_name)
    region_name = random.choice(regions)
    print(region_name)
    random_coords = generate_random_coords_in_region(country_name, 'Trööndelage', numb_stores)
    print(random_coords)
    exit()
    lat_lon = random.choice(random_coords)
    lat = lat_lon[0]
    lon = lat_lon[1]
    # cities = get_cities_in_region(country_name, region)
    # print(cities)
    for _ in range(numb_stores):
        store_data = {
            "store_id": fake.uuid4(),
            "store Name": fake.company(),
            "address": fake.street_address(),
            "city": fake.city(),
            "state_or_Province": region_name,
            "country": country_name,
            "postal/Zip Code": fake.zipcode(),
            "latitude": lat,
            "longitude": lon,
            "store_type": random.choice(["Supermarket", "Convenience Store", "Department Store"]),
            "opening_hours": "8:00 AM - 9:00 PM",
            "manager": fake.name(),
            "number_of_employees": random.randint(5, 100),
            "number_of_non_self_checkout_lanes": random.randint(2, 20),
            "number_of_self_checkout_lanes": random.randint(0, 4)
        }
        stores.append(store_data)
    stores_df = pd.DataFrame(stores)

    return stores_df





if __name__ == "__main__":
    pd.set_option('display.max_columns', None)
    # df = pd.read_parquet("products.parquet")
    # products = df["name"].unique().tolist()
    # pd.set_option('display.max_columns', None)  # None means unlimited columns
    # print(df.head())
    # exit()
    # Example usage
    numb_stores = 5
    country_name = "Norway"
    stores = generate_random_store_data(country_name, numb_stores)
    print(stores.head())


