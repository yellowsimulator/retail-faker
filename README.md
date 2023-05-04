# retail-faker

This is a package to generate fake retail data. It is based upon the python library Faker. Although still in development, you can start using it.

The main entry point is the module *retail_faker.py. This module relies on three other modules (helper_functions.py, stores.py, transactions.py, products.py), each one generating data for stores, products and transaction.* You can run this file and the program will generate three parquets files in the folder retail_data: *retail_data/products.parquet, retail_data/stores.parquet, retail_data/transactions.*

### Contribution

- clone the repo
- install requirement
- create a feature branch or improve it

### To do list

- Create a machine learning model that generate realistic product names based on country, product category and product subcategory
- Refactor the code and improve readability
- Refactor the code and improve performance
- clean up exception handling
- Use config files for products, transactions, and stores?
- Add/remove some tables from products, transactions and stores
- Add supplier tables
