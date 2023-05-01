
import pycountry
import yaml
import random
import pandas as pd
from faker import Faker
fake = Faker()

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
    for cat in categories_data['categories']:
        if category in cat:
            return cat[category]
    return []

def generate_products_for_category(category,
                                   num_products=10,
                                   yaml_file_path='product_categories.yaml') -> list:
    """Generates products for a given category.


    Parameters
    ----------
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

    for _ in range(num_products):
        product = {
            'id': fake.uuid4(),
            'name': fake.bs().title(),
            'description': fake.sentence(),
            'category': category,
            'subcategory': random.choice(subcategories),
            'brand': fake.company(),
            'price': round(random.uniform(1, 100), 2),
            #'weight': round(random.uniform(50, 5000), 2),  # Weight in grams
            'expiration_date': fake.date_between(start_date='+30d', end_date='+365d').strftime('%Y-%m-%d'),
        }
        products.append(product)

    return products


def generate_product_name(category, subcategory, num_keywords=2):
    keywords = {
        'Beverages': ['Coffee', 'Tea', 'Soda', 'Juice', 'Water', 'Energy Drink'],
        'Snacks & Sweets': ['Chocolate', 'Candy', 'Chips', 'Popcorn', 'Nuts', 'Cookies'],
        'Pantry Staples': ['Pasta', 'Rice', 'Canned Food', 'Sauce', 'Oil', 'Spices'],
        'Baking & Cooking Supplies': ['Flour', 'Sugar', 'Baking Soda', 'Yeast', 'Salt', 'Vinegar'],
        'Organic & Healthy Foods': ['Organic', 'Gluten-Free', 'Vegan', 'Vegetarian', 'Low-Fat', 'Non-GMO'],
        'International Foods': ['Italian', 'Indian', 'Mexican', 'Chinese', 'Japanese', 'Korean'],
        'Computers & Accessories': ['Laptop', 'Desktop', 'Monitor', 'Keyboard', 'Mouse', 'Printer'],
    }
    # keywords = {
    #     'Mobile Phones & Accessories': ['Smartphone', 'Case', 'Charger', 'Screen Protector', 'Headphones', 'Cable'],
    #     'Computers & Accessories': ['Laptop', 'Desktop', 'Monitor', 'Keyboard', 'Mouse', 'Printer'],
    #     'Audio & Video Equipment': ['Speaker', 'Headphones', 'Earbuds', 'Soundbar', 'Microphone', 'Projector'],
    #     'Cameras & Photography': ['Camera', 'Lens', 'Tripod', 'Memory Card', 'Flash', 'Bag'],
    #     'Gaming & Consoles': ['Console', 'Controller', 'Game', 'Headset', 'Keyboard', 'Mouse'],
    #     'Smart Home Devices': ['Smart Speaker', 'Smart Light', 'Smart Thermostat', 'Smart Plug', 'Smart Lock', 'Security Camera'],
    #     'Men\'s Clothing': ['Shirt', 'Pants', 'Jacket', 'Sweater', 'Shoes', 'Accessories'],
    #     'Women\'s Clothing': ['Dress', 'Blouse', 'Skirt', 'Pants', 'Shoes', 'Accessories'],
    #     'Children\'s Clothing': ['T-shirt', 'Pants', 'Dress', 'Sweater', 'Shoes', 'Accessories'],
    #     'Footwear': ['Sneakers', 'Boots', 'Sandals', 'Heels', 'Slippers', 'Flip-flops'],
    #     'Bags & Luggage': ['Backpack', 'Handbag', 'Luggage', 'Wallet', 'Briefcase', 'Duffle'],
    #     'Jewelry & Watches': ['Necklace', 'Earrings', 'Bracelet', 'Ring', 'Watch', 'Pendant'],
    #     'Eyewear': ['Sunglasses', 'Reading Glasses', 'Contact Lenses', 'Frames', 'Goggles', 'Accessories'],
    #     'Kitchen Appliances': ['Refrigerator', 'Microwave', 'Oven', 'Dishwasher', 'Mixer', 'Toaster'],
    #     'Home Appliances': ['Washing Machine', 'Dryer', 'Air Conditioner', 'Heater', 'Fan', 'Vacuum Cleaner'],
    #     'Cookware & Bakeware': ['Pot', 'Pan', 'Baking Dish', 'Spatula', 'Mixer', 'Measuring Cup'],
    #     'Tableware': ['Plate', 'Bowl', 'Cup', 'Cutlery', 'Serving Dish', 'Placemat'],
    #     'Storage & Organization': ['Shelf', 'Cabinet', 'Drawer', 'Box', 'Closet Organizer', 'Hanger'],
    #     'Home Decor & Furnishings': ['Cushion', 'Blanket', 'Curtain', 'Rug', 'Vase', 'Wall Art'],
    #     'Personal Care Appliances': ['Electric Toothbrush', 'Hair Dryer', 'Razor', 'Epilator', 'Trimmer', 'Straightener'],
    #     'Makeup & Cosmetics': ['Lipstick', 'Foundation', 'Mascara', 'Eyeliner', 'Blush', 'Nail Polish'],
    #     'Skincare': ['Cleanser', 'Moisturizer', 'Serum', 'Sunscreen', 'Toner', 'Mask'],
    #     'Hair Care': ['Shampoo', 'Conditioner', 'Hair Mask', 'Hair Oil', 'Styling Gel', 'Hairspray'],
    #     }

    category_keywords = keywords.get(category, [])
    subcategory_keywords = keywords.get(subcategory, [])

    selected_keywords = random.sample(category_keywords + subcategory_keywords, num_keywords)
    product_name = f"{selected_keywords[0]} {selected_keywords[1]} {fake.word()}"

    return product_name.title()



def save_products_to_parquet(products: list, file_path: str):
    df = pd.DataFrame(products)
    print(df.head())
    exit()
    df.to_parquet(file_path)

if __name__ == '__main__':
        # Example usage
    file_path = 'product_categories.yaml'
    #categories = load_categories_from_yaml(file_path)

    #sub_cats = load_subcategories_from_yaml(file_path, 'Electronics')
    products = generate_products_for_category('Electronics', 10)
    name = generate_product_name('Electronics', 'Computers & Accessories')
    print(name)
    #save_products_to_parquet(products, 'products.parquet')
    # country_name = 'Sweden'
    # country_code = get_country_code(country_name)
    # print(get_regions_of_country(country_code))