
import pycountry
import yaml
import random
import pandas as pd
import pandas as pd
import requests
from forex_python.converter import CurrencyRates
from forex_python.bitcoin import BtcConverter
from datetime import datetime, timedelta
import pycountry
from faker import Faker
from datetime import datetime
from tqdm import tqdm
fake = Faker()


from countryinfo import CountryInfo

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


def get_regions_of_country(country_code: str) -> list:
    """Returns the regions of a given country.

    Parameters
    ----------
        country_code: the country code to get the regions for

    Returns
    -------
        country_subdivisions: the regions of the given country
    """
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


def generate_products_for_category(country_name: str,
                                   category: str,
                                   num_products: int=10,
                                   yaml_file_path: str='product_categories.yaml') -> list:
    """Generates products for a given category.


    Parameters
    ----------
        country_name: the country to generate products for
        category: the category to generate products for
        num_products: the number of products to generate
        yaml_file_path: path to the yaml file

    Returns
    -------
        products: the generated products
    """
    subcategories = load_subcategories_from_yaml(yaml_file_path, category)

    if not subcategories:
        print(f"Category '{category}' not found in the YAML file.")
        return []
    products = []
    m = format(num_products, ',')
    inflation = get_inflation_rate(country_name)
    for _ in tqdm(range(num_products), desc=f"Generating {m} products for '{category}'"):
        subcategory = random.choice(list(subcategories.keys()))
        price_range = subcategories[subcategory]
        price_start, currency_code = convert_usd_to_local(price_range[0], country_name)
        price_end, _ = convert_usd_to_local(price_range[1], country_name)
        price_start = price_start * (1 + inflation)
        price_end = price_end * (1 + inflation)
        product = {
            'id': fake.uuid4(),
            'name': fake.bs().title(),
            'description': fake.sentence(),
            'category': category,
            'subcategory': random.choice(list(subcategories.keys())),
            'brand': fake.company(),
            'price': round(random.uniform(price_start, price_end), 2),
            'currency': currency_code,
            'expiration_date': fake.date_between(start_date='+30d', end_date='+365d').strftime('%Y-%m-%d'),
        }
        products.append(product)
    return products


def generate_product_name(category: str, subcategory: str, num_keywords: int=2):
    """Generates a product name from a given category and subcategory.


    Parameters
    ----------
        category: the category to generate a product name for
        subcategory: the subcategory to generate a product name for
        num_keywords: the number of keywords to use in the product name

    Returns
    -------
        product_name: the generated product name
    """
    keywords = {
        'Beverages': ['Coffee', 'Tea', 'Soda', 'Juice', 'Water', 'Energy Drink'],
        'Snacks & Sweets': ['Chocolate', 'Candy', 'Chips', 'Popcorn', 'Nuts', 'Cookies'],
        'Pantry Staples': ['Pasta', 'Rice', 'Canned Food', 'Sauce', 'Oil', 'Spices'],
        'Baking & Cooking Supplies': ['Flour', 'Sugar', 'Baking Soda', 'Yeast', 'Salt', 'Vinegar'],
        'Organic & Healthy Foods': ['Organic', 'Gluten-Free', 'Vegan', 'Vegetarian', 'Low-Fat', 'Non-GMO'],
        'International Foods': ['Italian', 'Indian', 'Mexican', 'Chinese', 'Japanese', 'Korean'],
        'Computers & Accessories': ['Laptop', 'Desktop', 'Monitor', 'Keyboard', 'Mouse', 'Printer'],
    }

    category_keywords = keywords.get(category, [])
    subcategory_keywords = keywords.get(subcategory, [])

    selected_keywords = random.sample(category_keywords + subcategory_keywords, num_keywords)
    product_name = f"{selected_keywords[0]} {selected_keywords[1]} {fake.word()}"

    return product_name.title()



def save_products_to_parquet(products: list, file_path: str) -> None:
    """Save products to a parquet file

    Parameters
    ----------
        products : a list of product as a dictionaries
        file_path : the path to the parquet file to save the products to
    """
    df = pd.DataFrame(products)
    print(df.head())
    df.to_parquet(file_path)



if __name__ == '__main__':
        # Example usage

    # Example usage:
    amount_usd = 10000000
    num_products = 5
    country_name = "Norway"  # Can also use country code like 'JP' or 'JPN'
    converted_amount, currency_code = convert_usd_to_local(amount_usd, country_name)
    print(f"{amount_usd} USD is equivalent to {converted_amount} {country_name}'s local currency.")


    file_path = 'product_categories.yaml'
    category = "Electronics"
    # subcategories = load_subcategories_from_yaml(file_path, category)

    products = generate_products_for_category(country_name, category, num_products)
    save_products_to_parquet(products, 'products.parquet')

    #categories = load_categories_from_yaml(file_path)

    #sub_cats = load_subcategories_from_yaml(file_path, 'Electronics')
    # products = generate_products_for_category('Electronics', 10)
    # name = generate_product_name('Electronics', 'Computers & Accessories')
    # print(name)
    #save_products_to_parquet(products, 'products.parquet')
    # country_name = 'Denmark'
    # country_code = get_country_code(country_name)

    inflation = get_inflation_rate(country_name)
    print(f"The inflation rate in {country_name} is {inflation}.")
    # print(df.head())
    # print(get_regions_of_country(country_code))