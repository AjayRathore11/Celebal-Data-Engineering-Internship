# End-to-End Delta Lake Data Pipeline (SCD Type 1 & Type 2)

A robust, local data engineering pipeline built using **PySpark** and **Delta Lake** to handle incremental data loads. This project demonstrates how to implement data cleaning, transaction-safe storage, and enterprise data warehousing patterns like Slowly Changing Dimensions (SCD) Type 1 and Type 2.

## 📌 Project Overview
In production data systems, source data changes constantly. This pipeline processes a master customer dataset and an incremental update dataset to showcase two distinct historical data tracking strategies:
* **SCD Type 1 (Overwrite):** Overwrites existing records with updated information (no history kept).
* **SCD Type 2 (Historical Log):** Retains full historical tracking by versioning records using active flags and timestamps.

---

## 🛠️ Tech Stack & Architecture
* **Language:** Python
* **Framework:** PySpark (Apache Spark)
* **Storage Format:** Delta Lake (Parquet with ACID transactions)
* **Environment:** Google Colab / Jupyter Notebooks

### Data Pipeline Flow
1. **Data Ingestion:** Loading raw CSV data into Spark DataFrames.
2. **Data Cleaning:** Removing null values and dropping exact duplicates.
3. **Bronze/Silver Storage:** Initializing the foundational Delta tables.
4. **Incremental Load (SCD 1):** Performing an upsert (`MERGE`) to keep current data fresh.
5. **Historical Tracking (SCD 2):** Executing advanced merge logic to track record changes over time using `start_date`, `end_date`, and `is_current` columns.
6. **Data Quality Validation:** Programmatically verifying row counts and checking for duplicates in active records before pushing to production.

---

## 📂 Repository Structure
```text
├── customer_pipeline.ipynb      # Complete PySpark & Delta Lake notebook
├── customer_master.csv          # Initial baseline customer data
├── customer_incremental.csv     # Day 2 update data containing modifications/new users
├── README.md                    # Project documentation
└── screenshots/                 # Execution and verification logs
    ├── data_loading/            # Raw data ingestion state
    ├── data_cleaning/           # Deduplicated data state
    ├── scd1/                    # Results of SCD Type 1 Merge
    ├── scd2/                    # Results of SCD Type 2 Historical Log
    └── validation/              # Automated data quality check output
