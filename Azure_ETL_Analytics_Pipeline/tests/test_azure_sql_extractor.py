import pyodbc
import pytest

from etl.azure_sql_extractor import extract_from_azure_sql


def test_invalid_sql_query():
    with pytest.raises(pyodbc.Error):
        extract_from_azure_sql(
            "SELECT * FROM table_that_does_not_exist"
        )