# Week 6: Spark Architecture & Advanced Data Pipelines

**Intern:** Ajay Singh Rathore  
**Domain:** Data Engineering  
**Program:** Celebal Excellence Internship Program (CEIP) 2026  

## 🎯 Objective
The goal of this week's module was to dive deep into Apache Spark's distributed architecture and build a highly efficient PySpark data processing pipeline. This involved mastering schema handling, data transformations, and understanding the performance implications of different storage formats.

## 📊 Dataset
* **Source File:** `jeans.csv` (E-commerce apparel data)
* **Description:** A raw dataset containing product details, messy pricing formats, and mixed data types, perfect for practicing real-world data cleansing and casting.

## 🧠 Key Theoretical Concepts Mastered
* **Spark Architecture:** Understood the roles of the Driver node, Cluster Manager, and Executor (Worker) nodes in distributed processing.
* **Lazy Evaluation & DAG:** Learned how Spark uses Directed Acyclic Graphs (DAGs) to plan and optimize query execution before triggering an Action.
* **Predicate Pushdown:** Applied early filtering techniques to minimize data shuffling and optimize memory usage.
* **Storage Optimization:** Analyzed the structural and performance differences between row-based formats (CSV) and columnar formats (Parquet).

## 🛠️ Pipeline Execution Steps
1. **Data Ingestion:** Loaded the raw dataset with `header=True` and `inferSchema=True`.
2. **Column Selection & Renaming:** Isolated the required columns and standardized naming conventions for readability.
3. **Data Type Casting:** Casted string values into correct numeric types (e.g., converting discount percentages to integers).
4. **Calculated Columns:** Engineered a new `calculated_finalPrice` column using PySpark mathematical functions to bypass corrupted CSV data.
5. **Data Cleansing:** Implemented `.dropna()` to eliminate null values in critical columns and filtered for high-rated products (Rating >= 4.0).
6. **Optimized Output:** Wrote the final processed DataFrame to both **CSV** and **Parquet** formats to demonstrate data persistence.

## 📂 Folder Structure
* `data/` : Contains the raw `jeans.csv` file.
* `notebook/` : Contains the Google Colab PySpark notebook (`.ipynb`) with the executed pipeline.
* `output/` : Contains the finalized, clean data stored in both `.csv` and `.parquet` directories.

---
*Note: `.show()` was utilized throughout the pipeline execution instead of `.collect()` to adhere to big data memory management best practices and prevent Driver node OOM errors.*
