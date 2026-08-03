import pandas as pd

from etl.transform import (
    transform_customers,
    transform_orders,
    transform_payment,
    transform_products,
)


def test_transform_products():
    Data = {
        "ProductID": [1, 1, 2],
        "ProductName": ["Laptop", "Laptop", None],
        "Category": ["Electronics", "Electronics", None],
        "Price": [50000, 50000, None]
    }
    df = pd.DataFrame(Data)
    result = transform_products(df)

    assert len(result) == 2
    assert result["price"].isna().sum() == 0
    assert result["product_name"].isna().sum() == 0
    assert result["category"].isna().sum() == 0
    
def test_transform_customer():
    data = {
        "CustomerID": [1, 1, 2],
        "CustomerName": ["Anooj", "Anooj", None],
        "Email": ["anooj@test.com", "anooj@test.com", None],
        "City": ["Chennai", "Chennai", None],
        "SignupDate": ["2026-01-01", "2026-01-01", "2026-02-01"]
    }
    
    df = pd.DataFrame(data)
    result = transform_customers(df)

    assert len(result) == 2
    assert result["customer_name"].isna().sum() == 0
    assert result["email"].isna().sum() == 0
    assert result["city"].isna().sum() == 0 
    
def test_transform_orders():
    """Test order data cleaning and transformation."""

    data = {
        "OrderID": [1, 1, 2],
        "CustomerID": [101, 101, 102],
        "ProductID": [10, 10, 20],
        "Quantity": [2, 2, 1],
        "OrderDate": [
            "2026-01-01",
            "2026-01-01",
            "2026-01-02"
        ]
    }

    df = pd.DataFrame(data)

    result = transform_orders(df)

    assert len(result) == 2
    assert result.isna().sum().sum() == 0
    assert pd.api.types.is_datetime64_any_dtype(result["order_date"])

def test_transform_payment():
    """Test payment data cleaning and transformation."""

    data = {
        "PaymentID": [1, 1, 2],
        "OrderID": [101, 101, 102],
        "PaymentMethod": ["UPI", "UPI", "Card"],
        "Status": ["completed", "completed", "pending"]
    }

    df = pd.DataFrame(data)

    result = transform_payment(df)

    assert len(result) == 2
    assert result.isna().sum().sum() == 0
    assert result["status"].tolist() == ["Completed", "Pending"]