import os

import pandas as pd
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")

blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

def upload_to_azure(df: pd.DataFrame, filename: str) -> None:
    """Upload a DataFrame as a CSV file to Azure Blob Storage."""
    
    csv_data = df.to_csv(index=False)
    blob_name = f"processed/{filename}"
    
    container_client.upload_blob(name = blob_name,
                                 data = csv_data,
                                 overwrite = True)