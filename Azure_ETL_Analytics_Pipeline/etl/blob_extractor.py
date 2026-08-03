import os
from io import BytesIO

import pandas as pd
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")

blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

def extract_from_blob(filename: str) -> pd.DataFrame:
    """
    Extract a CSV file from Azure Blob Storage and return it as a DataFrame.
    
    """
    blob_client = container_client.get_blob_client(filename)
    blob_data = blob_client.download_blob()
    data = blob_data.readall()
    df = pd.read_csv(BytesIO(data))
    return df