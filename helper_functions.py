import time
import yaml
import random
import requests
import pycountry
import pandas as pd
import pyarrow as pa
import geopandas as gpd
from pathlib import Path
import pyarrow.parquet as pq
from datetime import datetime
from shapely.geometry import Point
from countryinfo import CountryInfo
from forex_python.converter import CurrencyRates


def save_data(df: pd.DataFrame, file_path: str) -> None:
    """Creates a folder `retail_data` if it doesn't exist.
         Then saves the data in the folder as in :
            retail_data/`file_name.parquet`.

    Parameters
    ----------
        df: the data as a pandas DataFrame

    Returns
    -------
        None
    """
    folder_path = Path('retail_data')
    if not folder_path.exists():
        folder_path.mkdir()
    table = pa.Table.from_pandas(df)
    save_to = folder_path / file_path
    pq.write_table(table, save_to)
    return



def timer_decorator(func):
    """A decorator that prints the execution time of a function.

    Usage
    -----
    @timer_decorator
    def my_function():
        pass
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Execution time for {func.__name__}: {elapsed_time:.4f} seconds")
        return result
    return wrapper


def generate_random_coords_in_region(country_name: str,
                                     region_name: str, num_points: int):
    """Generates random latitude and longitude
       coordinates within a given region.

    Parameters
    ----------
        shapefile_path: path to the shapefile
        country_name: the country to generate coordinates for
        region_name: the region to generate coordinates for
        num_points: the number of coordinates to generate

    Returns
    -------
        random_points: the generated coordinates
    """
    shapefile_path = "shap/ne_10m_admin_1_states_provinces.shp"
    gdf = gpd.read_file(shapefile_path)

    region = gdf[(gdf['admin'] == country_name) & (gdf['name'] == region_name)].iloc[0]

    bbox = region.geometry.bounds
    min_x, min_y, max_x, max_y = bbox

    random_points = []
    while len(random_points) < num_points:
        random_lat = random.uniform(min_y, max_y)
        random_lng = random.uniform(min_x, max_x)
        point = Point(random_lng, random_lat)

        # Check if the point is within the region's geometry
        if region.geometry.contains(point):
            random_points.append((random_lat, random_lng))

    return random_points


def load_subcategories_from_yaml(category: str,
                                 file_path: str='configs/products_configs.yaml') -> dict:
    """Loads subcategories from a yaml file.

    Parameters
    ----------
        file_path: path to the yaml file
        category: the category to get the subcategories for

    Returns
    -------
        subcategories: the subcategories of the given category
    """
    file_path = Path(file_path)
    with open(file_path, 'r') as f:
        categories_data = yaml.safe_load(f)
    categories = categories_data['categories']
    if category in categories:
        return categories[category]
    return {}


def get_regions_of_country(country_name: str) -> list:
    """Returns the regions of a given country.

    Parameters
    ----------
        country_code: the country code to get the regions for

    Returns
    -------
        country_subdivisions: the regions of the given country
    """
    country_code = get_country_code(country_name)
    country_subdivisions = []
    for subdivision in pycountry.subdivisions.get(country_code=country_code):
        country_subdivisions.append(subdivision.name)
    return country_subdivisions


def load_categories_from_yaml(file_path: str='configs/products_configs.yaml') -> list:
    """Loads product categories from a yaml file.

    Parameters
    ----------
        file_path: path to the yaml file

    Returns
    -------
        categories: the product categories
    """
    file_path = Path(file_path)
    with open(file_path, 'r') as f:
        categories_data = yaml.safe_load(f)
    categories = list(categories_data['categories'].keys())
    return categories


def get_country_code(country_name: str) -> str:
    """Returns the country code for a given country name

    Parameters
    ----------
        country_name: name of the country to get the code for

    Returns
    -------
        country_code: the country code for the given country name
    """
    try:
        country = pycountry.countries.get(name=country_name)
        return country.alpha_2
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_currency_code(country_name: str) -> str:
    """Returns the currency code for a given country name.


    Parameters
    ----------
        country_name: the name of the country to get the currency code for

    Returns
    -------
        currency_code: the currency code for the given country name
    """
    try:
        country_obj = pycountry.countries.search_fuzzy(country_name)[0]
        country_info = CountryInfo(country_obj.name)
        currency_code = country_info.currencies()[0]
        return currency_code
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_exchange_rate(country_name: str) -> float:
    """Returns the exchange rate for a given country name.
    """
    country_currency_code = get_currency_code(country_name)
    currency_rates = CurrencyRates()
    try:
        exchange_rate = currency_rates.get_rate(country_currency_code, 'USD')
        return exchange_rate
    except Exception as e:
        print(f"Error fetching exchange rate for {country_currency_code}: {e}")
        return None


def convert_usd_to_local(amount_usd: float, country_name: str) -> float:
    """Converts an amount from USD to the local currency of a given country.

    Parameters
    ----------
        amount_usd: the amount in USD to convert
        country: the country to convert the amount to

    Returns
    -------
        converted_amount: the amount in the local currency

    Examples
    --------
        >>> country = "Japan"  # or "JP" or "JPN"
        >>> amount_usd = 100
        >>> convert_usd_to_local(amount_usd, country)
    """
    cr = CurrencyRates()
    currency_code = get_currency_code(country_name)
    try:
        converted_amount = cr.convert('USD', currency_code, amount_usd)
        return round(converted_amount, 2), currency_code
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_inflation_rate(country_name: str) -> pd.DataFrame:
    """Returns the inflation rate for a given country name.

    Parameters
    ----------
        country_code: the country code to get the inflation rate for
    Returns
    -------
        df: the inflation rate for the given country code and time period
    """
    start_year = datetime.now().year - 2
    end_year = datetime.now().year
    country_code = get_country_code(country_name)
    url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/FP.CPI.TOTL.ZG?format=json&date={start_year}:{end_year}"
    response = requests.get(url)
    data = response.json()

    if data[0] is not None:
        df = pd.DataFrame(data[1])
        df = df[['countryiso3code', 'date', 'value']]
        df.columns = ['Country Code', 'Year', 'Inflation Rate']
        inflation_rate = df['Inflation Rate'].iloc[0]
        return inflation_rate/100.0
    return None


def get_cities_in_subdivision(country_name: str,
                              subdivision_name: str,
                              username: str='retail_faker') -> list:
    """Returns the cities in a given subdivision of a given country.

    Parameters
    ----------
        country_name: the name of the country to get the cities for
        subdivision_name: the name of the subdivision to get the cities for
        username: the username to use for the GeoNames API

    Returns
    -------
        cities: the cities in the given subdivision of the given country

    Nonte
    -----
    This function is not working properly yet!
    """
    url = "http://api.geonames.org/searchJSON"
    country_code = get_country_code(country_name)
    params = {
        "country": country_code,
        "adminName1": subdivision_name,
        "featureClass": "P",  # Populated place
        "username": username,
        "maxRows": 1000,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        cities = [city["name"] for city in data["geonames"]]
        return cities
    else:
        raise ValueError(f"Error fetching data from GeoNames API: {response.status_code}")





if __name__=='__main__':

    categories = load_categories_from_yaml()
    category = 'Electronics'
    subcategories = load_subcategories_from_yaml(category)
    print(subcategories)
#    print(cities)

