# Week 5: Apache Spark Fundamentals

**Objective:** Learn the basics of Apache Spark and build a data pipeline using PySpark DataFrames.

### Steps Performed:
1. **Loaded Data:** Read a CSV file into a Spark DataFrame using `escape='"'` to safely handle commas inside product names.
2. **Data Cleaning:** Used `.dropDuplicates()` and `.dropna()` to remove exact duplicate rows and handle missing values.
3. **Transformations:** Casted the 'Sales' column from a String data type to a Double (decimal) to fix formatting issues.
4. **Filtering:** Applied multiple conditions to isolate Furniture sales in the West region that were $100 or greater.
5. **Aggregation:** Grouped the cleaned data by `Region` and used functions like `count`, `sum`, `avg`, `min`, and `max` to create a business summary table.

### Observations:
* I observed that Spark DataFrames are immutable. When I applied the cleaning functions, I had to save the result to a new variable (`cleaned_df`) to preserve the pipeline.
* Dealing with real-world CSV files requires careful ingestion. I noticed that unescaped commas in product names can shift columns, which throws a "CAST_INVALID_INPUT" error when trying to change data types.
* Wide transformations like `groupBy` successfully summarized the data, but I learned that this triggers a "shuffle" (data movement across partitions), which is an expensive operation in Spark.
