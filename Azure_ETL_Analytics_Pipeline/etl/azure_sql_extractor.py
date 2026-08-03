import os
import struct

import pandas as pd
import pyodbc
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

AZURE_SQL_SERVER = os.getenv("AZURE_SQL_SERVER")
AZURE_SQL_DATABASE = os.getenv("AZURE_SQL_DATABASE")

def extract_from_azure_sql(query: str) -> pd.DataFrame:
    """Extract data from Azure SQL into a Pandas DataFrame."""
    
    credential = AzureCliCredential()
    token = credential.get_token(
        "https://database.windows.net/.default"
    ).token
    
    token_bytes = token.encode("utf-16-le")

    token_struct = (
        struct.pack("<I", len(token_bytes))
        + token_bytes
    )
    connection_string = (
        "DRIVER=/opt/homebrew/lib/libmsodbcsql.18.dylib;"
        f"SERVER=tcp:{AZURE_SQL_SERVER},1433;"
        f"DATABASE={AZURE_SQL_DATABASE};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
    )
    SQL_COPT_SS_ACCESS_TOKEN = 1256
    with pyodbc.connect(
        connection_string,
        attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct},
        timeout=30
    ) as conn:
        df = pd.read_sql(query, conn)

    return df

if __name__ == "__main__":
    df = extract_from_azure_sql(
        "SELECT * FROM products"
    )

    print(df)