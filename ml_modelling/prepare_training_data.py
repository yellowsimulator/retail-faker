import pandas as pd
# map the (product category, productt subcategory) to  (a product name)
# input_text = "Grocery & Gourmet Foods, Beverages"
# output_text = "Sparkling Mineral Water"
train_data = [
    ("generate product name:  1 Grocery & Gourmet Foods,  1 Beverages", "Organic Green Tea Bags"),
    ("generate product name:  2 Grocery & Gourmet Foods, 2 Snacks & Sweets", "Chocolate Chip Cookies"),
    ("generate product name: 3 Grocery & Gourmet Foods, 3 Pantry Staples", "Extra Virgin Olive Oil"),
    ("generate product name: 4 Grocery & Gourmet Foods, 4 Baking & Cooking Supplies", "Pure Vanilla Extract"),
    ("generate product name: 5 Grocery & Gourmet Foods, 5 Organic & Healthy Foods", "Gluten-Free Quinoa Pasta"),
    ("generate product name: 6 Grocery & Gourmet Foods, 6 International Foods", "Italian Tomato Basil Pasta Sauce"),
    ("generate product name: 7 Grocery & Gourmet Foods, 7 Beverages", "Cold Brew Coffee Concentrate"),
    ("generate product name: 8 Grocery & Gourmet Foods, 8 Snacks & Sweets", "Sour Gummy Worms"),
    ("generate product name: 9 Grocery & Gourmet Foods, 9 Pantry Staples", "Raw Almonds"),
    ("generate product name: 10 Grocery & Gourmet Foods, 10 Baking & Cooking Supplies", "Organic Coconut Sugar"),
    ("generate product name: 11 Grocery & Gourmet Foods, 11 Organic & Healthy Foods", "Vegan Protein Powder"),
    ("generate product name: 12 Grocery & Gourmet Foods, 12 International Foods", "Japanese Ramen Noodles")
]

validation_data = [
    ("generate product name: 1 Grocery & Gourmet Foods, 1 Beverages", "Sparkling Mineral Water"),
    ("generate product name: 2 Grocery & Gourmet Foods, 2 Snacks & Sweets", "Sea Salt Caramel Popcorn"),
    ("generate product name: 3 Grocery & Gourmet Foods, 3 Pantry Staples", "Organic Apple Cider Vinegar"),
    ("generate product name: 4 Grocery & Gourmet Foods, 4 Baking & Cooking Supplies", "Unsweetened Cocoa Powder"),
    ("generate product name: 5 Grocery & Gourmet Foods, 5 Organic & Healthy Foods", "Organic Dried Cranberries"),
    ("generate product name: 6 Grocery & Gourmet Foods, 6 International Foods", "Authentic Mexican Salsa")
]

df = pd.DataFrame(train_data, columns=["input_text", "target_text"])
df.to_csv("train.csv", index=False)
validation_df = pd.DataFrame(validation_data, columns=["input_text", "target_text"])
validation_df.to_csv("validation.csv", index=False)
