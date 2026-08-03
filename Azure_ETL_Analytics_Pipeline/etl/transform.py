import pandas as pd


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Convert DataFrame column names from CamelCase to snake_case."""
    
    df.columns=(df.columns
                .str.strip()
                .str.replace(r"([a-z0-9])([A-Z])", r"\1_\2", regex=True)
                .str.lower())
    return df

def transform_products(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and transform product data."""
    
    df = clean_column_names(df)
    
    df.drop_duplicates(inplace = True)
    
    df['price'] = df['price'].fillna(0)
    df['product_name'] = df['product_name'].fillna('Unknown')
    df['category'] = df['category'].fillna('Unknown')
    
    return df
    
def transform_customers(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and transform customer data."""
    
    df = clean_column_names(df)
    
    df.drop_duplicates(inplace = True)
    
    df['email'] = df['email'].fillna("Not Available")
    df['customer_name'] = df['customer_name'].fillna("Unknown")
    df['city'] = df['city'].fillna("Unknown")
    df.dropna(subset=["signup_date"],inplace = True)
    
    return df

def transform_orders(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and transform order data."""
    
    df = clean_column_names(df)
    
    df.drop_duplicates(inplace = True)
    
    df.dropna(inplace = True)
    df['order_date'] = pd.to_datetime(df['order_date'])
    
    return df

def transform_payment(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and transform payment data."""
    
    df = clean_column_names(df)
    
    df.drop_duplicates(inplace = True)
    
    df.dropna(inplace=True)
    df['status'] = df['status'].str.title()
    
    return df

