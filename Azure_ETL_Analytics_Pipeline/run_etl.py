import logging
import os

from dotenv import load_dotenv

load_dotenv()
PRODUCTS_FROM_AZURE_SQL = (
    os.getenv("PRODUCTS_FROM_AZURE_SQL", "false").lower() == "true"
)

DATABASE_NAME = os.getenv("DATABASE_NAME")
DATA_FOLDER = os.getenv("DATA_FOLDER")
LOG_FILE = os.getenv("LOG_FILE")

logging.basicConfig(filename = LOG_FILE, level = logging.INFO, format = "%(asctime)s - %(levelname)s - %(message)s", force = True)
logger = logging.getLogger(__name__)

from etl.azure_loader import upload_to_azure
from etl.azure_sql_extractor import extract_from_azure_sql
from etl.blob_extractor import extract_from_blob
from etl.emailer import send_mail
from etl.loader import load
from etl.report import reporting
from etl.transform import (
    transform_customers,
    transform_orders,
    transform_payment,
    transform_products,
)
from etl.viz import generate_visuals


def run_stage(stage_name: str, function, *args):
    """Run an ETL stage and log its success or failure."""
    
    try:
        result = function(*args)
        logger.info(f"{stage_name} completed successfully")
        return result
    except Exception:
        logger.exception(f"{stage_name} failed")
        raise
        


try:
    print("="*40)
    print("ETL PIPELINE STARTED")
    logger.info("ETL PIPELINE STARTED")
    print("="*40)

    print("\nExtracting Products...")
    logger.info("Extracting Products...")
    if PRODUCTS_FROM_AZURE_SQL:
        product_df = run_stage(
            "Product Azure SQL Extraction",
            extract_from_azure_sql,
            "SELECT * FROM products"
        )
    else:
        product_df = run_stage("Product Extraction",
                                extract_from_blob,
                                "Products.csv")
    print("Products Extracted")
    logger.info("Product Extracted successfully")
    
    product_df = run_stage("Products Transformation",
                           transform_products,
                           product_df)
    print("Products transformed ")
    logger.info("Product transformed successfully")
    
    run_stage("Product Azure Upload",
              upload_to_azure,
              product_df,
              "products_clean.csv")
    
    run_stage("Products SQLite Load",
              load,
              product_df,
              "products")
    print("Products loaded")
    logger.info("Products loaded into SQLite")

    print("\nReading Customers.csv...")
    logger.info("\nReading Customers.csv...")
    customer_df = run_stage("Customer Extraction",
                            extract_from_blob,
                            "Customers.csv")
    print("Customers Extracted")
    logger.info("Customers Extracted successfully")
    
    customer_df = run_stage("Customers Transformation",
                            transform_customers,
                            customer_df)
    print("Customers transformed")
    logger.info("Customers transformed successfully")
    
    run_stage("Customers Azure Upload",
              upload_to_azure,
              customer_df,
              "Customers_clean.csv")
    
    run_stage("Customer SQLite Load",
              load,
              customer_df,
              "customers")
    print("Customers loaded")
    logger.info("Customers loaded into SQLite")

    print("\nReading Orders.csv...")
    logger.info("\nReading Orders.csv...")
    orders_df = run_stage("Order Extraction",
                          extract_from_blob,
                          "Orders.csv")
    print("Orders Extracted")
    logger.info("Orders Extracted successfully")
    
    orders_df = run_stage("Orders Transformation",
                          transform_orders,
                          orders_df)
    print("Orders transformed")
    logger.info("Orders transformed successfully")
    
    run_stage("Orders Azure Upload",
              upload_to_azure,
              orders_df,
              "Orders_clean.csv")
    
    run_stage("Orders SQLite Load",
              load,
              orders_df,
              "orders")
    print("Orders loaded")
    logger.info("Orders loaded into SQLite")

    print("\nReading Payments.csv...")
    logger.info("\nReading Payments.csv...")
    payment_df = run_stage("Payments Extraction",
                           extract_from_blob,
                           "Payments.csv")
    print("Payments Extracted")
    logger.info("Payments Extracted successfully")
    
    payment_df = run_stage("Payments Transformation",
                           transform_payment,
                           payment_df)
    print("Payments transformed")
    logger.info("Payments transformed successfully")
    
    run_stage("Payments Azure Upload",
              upload_to_azure,
              payment_df,
              "Payments_clean.csv")
    
    run_stage("Payment SQLite Load",
              load,
              payment_df,
              "payments")
    print("Payments loaded")
    logger.info("Payments loaded into SQLite")

    print("="*40)
    print("ETL PIPELINE COMPLETED")
    logger.info("ETL PIPELINE COMPLETED")
    print("="*40)
    
    reporting()
    generate_visuals()
    send_mail("ETL Pipeline Success",
              "ETL Pipeline Completed Successfully",
              attach_report=True)
    
except Exception as e:
    print(f"ETL Pipeline failed: {e}")
    logger.exception("ETL Pipeline failed")
    
    send_mail("ETL Pipeline failed",
              f"The ETL Pipeline failed \n\n Error: {e}"
              )