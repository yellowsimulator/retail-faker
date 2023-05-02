import pycountry
import pandas as pd
import yaml
import requests
from datetime import datetime
from countryinfo import CountryInfo
from forex_python.converter import CurrencyRates
import geonamescache

import geopandas as gpd
import random
from shapely.geometry import Point

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

    # Find the specified region in the shapefile
    region = gdf[(gdf['admin'] == country_name) & (gdf['name'] == region_name)].iloc[0]

    # Get the bounding box of the region
    bbox = region.geometry.bounds
    min_x, min_y, max_x, max_y = bbox

    # Generate random latitude and longitude coordinates within the bounding box
    random_points = []
    while len(random_points) < num_points:
        random_lat = random.uniform(min_y, max_y)
        random_lng = random.uniform(min_x, max_x)
        point = Point(random_lng, random_lat)

        # Check if the point is within the region's geometry
        if region.geometry.contains(point):
            random_points.append((random_lat, random_lng))

    return random_points




def load_subcategories_from_yaml(file_path: str, category: str) -> dict:
    """Loads subcategories from a yaml file.

    Parameters
    ----------
        file_path: path to the yaml file
        category: the category to get the subcategories for

    Returns
    -------
        subcategories: the subcategories of the given category
    """
    with open(file_path, 'r') as f:
        categories_data = yaml.safe_load(f)

    # Access the 'categories' key directly, as the new YAML format has a 'categories' key at the top level
    categories = categories_data['categories']

    # Check if the requested category exists in the categories dictionary, and return its subcategories if it does
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


def load_categories_from_yaml(file_path: str) -> list:
    """Loads product categories from a yaml file.

    Parameters
    ----------
        file_path: path to the yaml file

    Returns
    -------
        categories: the product categories
    """
    with open(file_path, 'r') as f:
        categories_data = yaml.safe_load(f)
    categories = []
    for category in categories_data['categories']:
        categories.extend(category.keys())
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
    country = pycountry.countries.get(name=country_name)
    return country.alpha_2


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
    """Returns the inflation rate for a given country code and time period.

    Parameters
    ----------
        country_code: the country code to get the inflation rate for
        start_year: the start year of the time period
        end_year: the end year of the time period

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
    else:
        print("Data not available.")



def get_cities_in_subdivision(country_name, subdivision_name, username='retail_faker'):
    url = "http://api.geonames.org/searchJSON"
    country_code = get_country_code(country_name)
    params = {
        "country": country_code,
        "adminName1": subdivision_name,
        "featureClass": "P",  # Populated place
        "username": username,
        "maxRows": 1000,  # Increase or decrease as needed
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        cities = [city["name"] for city in data["geonames"]]
        return cities
    else:
        raise ValueError(f"Error fetching data from GeoNames API: {response.status_code}")









if __name__=='__main__':
    shapefile_path = "shap/ne_10m_admin_1_states_provinces.shp"  # Replace with the path to your shapefile
    country_name = "United States of America"
    region_name = "California"
    num_points = 100

    random_coords = generate_random_coords_in_region(shapefile_path, country_name, region_name, num_points)
    print(random_coords)



    country_name = "Norway"
    subdivision_name = "California"

#    cities = get_cities_in_subdivision(country_name, subdivision_name)
#    print(cities)

