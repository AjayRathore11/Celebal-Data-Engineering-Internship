# Week 4: Azure Cloud Fundamentals and Data Pipeline

**Celebal Excellence Internship Program (CEIP) 2026**  
**Domain:** Data Engineering  
**Submitted By:** Ajay Singh Rathore  

## Objective
To learn Azure cloud basics and build an end-to-end data pipeline using an Azure Storage Account and Azure Data Factory (ADF).

## Project Summary
In this mini-project, I built a complete cloud data pipeline to move data securely from a source to a destination. Here is a simple breakdown of the architecture and execution process:

* **Storage Setup:** Created a central Resource Group and an Azure Storage Account. Inside the storage account, I created a `raw-data` container and uploaded the initial `Sample - Superstore.csv` dataset.
* **Data Factory Setup:** Created an Azure Data Factory (ADF) workspace. I set up a Linked Service to securely connect ADF to my storage account and created source and destination datasets.
* **Pipeline Architecture:** Designed a pipeline that first uses a "Get Metadata" activity to check the source file's existence and size. This is connected to a "Copy Data" activity that automatically moves the file into a new `output` folder.
* **Execution & Results:** Successfully ran the pipeline in Debug mode. Verified the execution results by checking the storage account and confirming the new file was successfully copied to the output container. 
* **Security (IAM):** Assigned the "Storage Blob Data Contributor" role to the Data Factory to ensure it has official, secure permission to read and write data.
