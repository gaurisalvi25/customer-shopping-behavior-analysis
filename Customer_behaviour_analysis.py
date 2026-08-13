import pandas as pd

# Load dataset
df = pd.read_csv('customer_shopping_behavior.csv')

# Initial data inspection
#print(df.head())
#print(df.info())
#print(df.describe())
#print(df.describe(include='all'))
#print(df.isnull().sum())

# Handle missing review ratings using category-wise median
df['Review Rating'] = df['Review Rating'].fillna(
    df.groupby('Category')['Review Rating'].transform(
        lambda x: x.fillna(x.median())
    )
)

#print(df.isnull().sum())

# Standardize column names
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ', '_')
df = df.rename(columns={'purchase_amount_(usd)': 'purchase_amount'})

#print(df.columns)

# Create age groups
labels = ['Young Adult', 'Adult', 'Middle Aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels=labels)

#print(df[['age', 'age_group']].head(10))

# Convert purchase frequency to days
frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90,
}

df['purchase_frequency_days'] = df['frequency_of_purchases'].map(
    frequency_mapping
)

#print(df[['frequency_of_purchases', 'purchase_frequency_days']].head(10))

# Check whether discount and promo code usage are identical
#print((df['discount_applied'] == df['promo_code_used']).all())

# Remove redundant promo code column
df = df.drop('promo_code_used', axis=1)

#print(df.columns)

# Database connection setup
from sqlalchemy import create_engine

username = "root"
password = "gauri25"
host = "localhost"
port = "3306"
database = "customer_behaviour"

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
)

#print("Database connection successful!")

# Load cleaned DataFrame into MySQL
table_name = 'customer'

df.to_sql(
    name=table_name,
    con=engine,
    if_exists='replace',
    index=False
)

print(f"Data successfully loaded into table '{table_name}' in database '{database}'.")