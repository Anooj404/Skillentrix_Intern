import os
import sqlite3 as sq

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DATABASE_NAME = os.getenv("DATABASE_NAME")

def load(df: pd.DataFrame ,table_name: str) -> None:
    """Load a DataFrame into a SQLite database table."""
    
    with sq.connect(DATABASE_NAME) as conn:
        df.to_sql(
            table_name,
            conn, 
            if_exists = "replace",
            index = False)
   