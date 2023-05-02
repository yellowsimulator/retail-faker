
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
from countryinfo import CountryInfo
fake = Faker()

from helper_functions import get_currency_code
from helper_functions import convert_usd_to_local
from helper_functions import get_inflation_rate
from helper_functions import get_currency_code
from helper_functions import load_subcategories_from_yaml


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
            'product_name': fake.bs().title(),
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