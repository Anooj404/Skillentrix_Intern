# ETL Pipeline with Cloud Integration & Automated Reporting

## 1. Project Overview

This project implements an end-to-end ETL (Extract, Transform, Load) pipeline using Python and Microsoft Azure.

The pipeline supports multiple data sources, including Azure Blob Storage and Azure SQL Database. Extracted data is converted into Pandas DataFrames, cleaned and transformed, stored in SQLite and Azure Blob Storage, analyzed using SQL and Matplotlib, and distributed automatically through email reports.

The project follows a modular architecture where extraction, transformation, loading, reporting, visualization, and email operations are separated into independent Python modules.

---

## 2. System Architecture

The pipeline follows the architecture:

```text
                    ┌─────────────────────┐
                    │  Azure SQL Database │
                    │      Products       │
                    └──────────┬──────────┘
                               │
                      Encrypted ODBC
                     Microsoft Entra
                               │
                               ▼
┌─────────────────────┐    Python / Pandas
│ Azure Blob Storage  │──────────┐
│ Raw CSV Files       │          │
└─────────────────────┘          ▼
                        ┌──────────────────┐
                        │ Transformation   │
                        │ & Data Cleaning  │
                        └────────┬─────────┘
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
             SQLite Database          Azure Blob Storage
                                      Processed CSV Files
                    │
                    ▼
               SQL Analytics
                    │
                    ▼
                Matplotlib
                    │
                    ▼
              HTML/PDF Report
                    │
                    ▼
             Email Distribution

---

## 3. Multi-Source Extraction

The pipeline supports multiple cloud-based input sources.

### Azure Blob Storage

Raw CSV datasets are extracted from Azure Blob Storage using the Azure Storage SDK.

The pipeline processes:

- Products
- Customers
- Orders
- Payments

The downloaded CSV data is converted into Pandas DataFrames for transformation.

### Azure SQL Database

The Products dataset can alternatively be extracted from Azure SQL Database using an encrypted ODBC connection.

The extraction source is controlled through the environment variable:

```env
PRODUCTS_FROM_AZURE_SQL=true
```

When enabled, the pipeline executes:

```sql
SELECT * FROM products
```

When disabled, Products are extracted from the existing Azure Blob Storage CSV source.

Both extraction methods return a Pandas DataFrame, allowing the same transformation logic to operate independently of the source.

---

## 4. Azure SQL Connectivity and Security

Azure SQL connectivity is implemented using:

- Microsoft ODBC Driver 18 for SQL Server
- pyodbc
- Microsoft Entra authentication
- AzureCliCredential
- Azure SQL access tokens
- Encrypted database connections

The pipeline obtains an access token through Microsoft Entra authentication and passes the token to the ODBC driver.

The connection uses:

```text
Encrypt=yes
TrustServerCertificate=no
```

Database passwords are not hardcoded into the Python source code.

---

## 5. Data Transformation

Extracted datasets are processed using Pandas.

The transformation layer performs operations such as:

- Standardizing column names
- Handling missing values
- Removing duplicate records
- Cleaning inconsistent data
- Converting required data types
- Preparing structured datasets for loading

Separate transformation functions are used for Products, Customers, Orders, and Payments.

---

## 6. Data Loading

After transformation, cleaned data is persisted to multiple destinations.

### SQLite

Structured datasets are loaded into a local SQLite database for SQL-based storage and analytics.

### Azure Blob Storage

Processed datasets are converted back into CSV format and uploaded to Azure Blob Storage.

This provides both relational and cloud object-storage targets.

---

## 7. Analytics and Reporting

The pipeline generates analytics from the processed data.

SQL queries and Pandas operations are used to calculate analytical results.

Matplotlib is used to generate visualizations.

The pipeline then produces:

- Analytics charts
- HTML reports
- PDF reports

The generated reports are stored in the reports directory.

---

## 8. Automated Email Distribution

After successful pipeline execution, the generated PDF analytics report is automatically distributed through email.

SMTP is used for email delivery.

The pipeline also supports failure notifications so that errors during execution can be reported automatically.

Email credentials are stored in environment variables instead of being hardcoded into the source code.

---

## 9. Logging and Error Handling

Pipeline execution is monitored using Python logging.

Individual pipeline stages use exception handling so that failures can be identified and recorded.

The pipeline handles scenarios such as:

- Missing Azure Blob source files
- Invalid Azure SQL queries
- Database connection failures
- Transformation errors
- Report generation failures
- Email delivery failures

---

## 10. Automated Testing

Pytest is used to validate important pipeline functionality.

The test suite includes:

- Product transformation testing
- Customer transformation testing
- Order transformation testing
- Payment transformation testing
- Missing Azure Blob source testing
- Invalid Azure SQL query testing

All six automated tests pass successfully.

Tests can be executed using:

```bash
python3 -m pytest -v
```
---

## 11. Installation and Setup

### Prerequisites

The project requires:

- Python 3
- Git
- Azure Storage Account
- Azure SQL Database
- Azure CLI
- Microsoft ODBC Driver 18 for SQL Server
- unixODBC
- Microsoft Entra account with access to Azure SQL

### Install Python Dependencies

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

### Environment Configuration

Create the local environment file from the provided template:

```bash
cp .env.example .env
```

Configure the required Azure Storage, Azure SQL, database, and email settings inside `.env`.

Sensitive credentials must never be committed to Git.

### Azure SQL Authentication

Sign in to Azure CLI:

```bash
az login
```

The pipeline uses Microsoft Entra authentication to obtain an Azure SQL access token.

To use Azure SQL as the Products source:

```env
PRODUCTS_FROM_AZURE_SQL=true
```

To use the Blob/CSV source:

```env
PRODUCTS_FROM_AZURE_SQL=false
```

---

## 12. Running the Pipeline

Execute the complete ETL pipeline from the project root:

```bash
python3 run_etl.py
```

The pipeline will:

1. Extract source data.
2. Transform and clean the datasets.
3. Load structured data into SQLite.
4. Upload processed data to Azure Blob Storage.
5. Generate analytics and visualizations.
6. Generate HTML and PDF reports.
7. Send the generated report through email.
8. Record pipeline execution in log files.

---

## 13. Running Tests

Run the complete automated test suite:

```bash
python3 -m pytest -v
```

The test suite validates transformation logic and important extraction failure scenarios.

---

## 14. Project Structure

```text
ETL_project/
│
├── etl/
│   ├── azure_sql_extractor.py
│   ├── blob_extractor.py
│   ├── transform.py
│   ├── loader.py
│   ├── azure_loader.py
│   ├── report.py
│   ├── viz.py
│   └── emailer.py
│
├── tests/
│   ├── test_transform.py
│   ├── test_azure_sql_extractor.py
│   └── test_blob_extractor.py
│
├── data_backup/
├── reports/
│
├── .env.example
├── .gitignore
├── requirements.txt
├── run_etl.py
├── README.md
└── CAPSTONE_PROJECT.md
```

---

## 15. Conclusion

This project demonstrates a complete cloud-integrated ETL workflow using Python and Microsoft Azure.

It combines multi-source extraction, Pandas-based transformation, hybrid data storage, Azure SQL connectivity through encrypted ODBC, Microsoft Entra authentication, automated analytics, report generation, email distribution, logging, error handling, and automated testing.

The modular architecture allows individual pipeline components to be maintained and extended independently.