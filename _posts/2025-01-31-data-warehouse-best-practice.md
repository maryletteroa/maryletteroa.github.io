---
layout: post
title: Data Warehousing Best Practices
categories: [learning-log]
tags: [data-engineering]
---

Here are some notes[^1] on DW Best Practices. Good points to keep in mind but admittedly warrants more concrete examples and unpacking (more in the future, so this could be an evolving note).

## Table Design Best Practices

- **Normalization and Denormalization**
    - Use *normalization* to reduce data redundancy and improve data integrity. 
    - Balance it with *denormalization* for query performance in read-heavy scenarios.
- **Partitioning**
    - Improves query performance and manageability.
    - Choose appropriate partitioning keys based on query patterns.
- **Indexing** 
    - Speeds up query performance.
    - Create indexes on columns that are frequently used in WHERE clauses, JOIN conditions, and ORDER BY clauses.
    - See [Sargable](https://en.wikipedia.org/wiki/Sargable) SQL queries.
- **Primary and Foreign Keys**
    - Define *primary keys* to uniquely identify each row
    - *Foreign keys* to maintain referential integrity between tables.
- **Surrogate Keys**
    - Consider using *surrogate keys* (e.g., auto-increment integers, hash keys) instead of natural keys for primary keys
    - Avoid issues with changing natural key values.
- **Column Data Types**
    - Choose appropriate data types for each column to optimize storage and performance.
    - Avoid using large data types unless necessary.
- **Data Compression** 
    - Implement data compression techniques to save storage space and improve I/O performance.
- **Audit Columns**
    - Include audit columns (e.g., `created_at`, `updated_at`) to track record creation and modification times.
- **Naming Conventions**
    - Follow consistent naming conventions for tables, columns, and other database objects to improve readability and maintainability.
    - See [SQL Style Guide](https://www.sqlstyle.guide/) by Simon Holywell
- **Avoid Nulls**
    - Minimize the use of `NULL` values as they can complicate queries and data processing
    - Use default values where applicable.


## Data Warehouse Design Guidelines

- **Understand Business Goals**
    - Clearly define the business objectives and requirements that the data warehouse aims to address
- **Data Governance**
    - Establish strong data governance policies to ensure data quality, security, and compliance
    - A Medium article about securing PII [Secure PII in Data Warehouse using BigQuery, Dataplex, MS Entra ID](https://medium.com/@tarik.sm/all-you-need-to-know-to-secure-pii-in-a-data-wharehouse-using-bigquery-dataplex-ms-entra-id-and-98ed31ac22d5)
    - [Using Iceberg data format in Athena to implement GDPR use-cases](https://aws.amazon.com/blogs/big-data/build-a-real-time-gdpr-aligned-apache-iceberg-data-lake/
    )
- **Metadata Management**
    - Properly manage metadata to organize and document data assets, making them easily accessible
- **Scalability**
    - Design the data warehouse with scalability in mind to accommodate future growth and increasing data volumes
- **Performance Optimization**
    - Regularly monitor and tune query performance using techniques like partitioning and indexing
- **Security Measures**
    - Implement advanced security measures such as encryption, access control, and authentication to protect sensitive information
- **Automation**
    - Automate processes like data transformation and model creation to reduce manual errors and improve efficiency
- **Agile Approach**
    - Adopt an agile methodology to allow for rapid adjustments and continuous improvement
- **Data Quality Assurance**
    - Implement robust data cleansing and validation processes to ensure high data quality
- **Data Lifecycle Management**
    - Define strategies for data archival and purging to keep the data warehouse lean and efficient

#### Footnotes
[^1]: Written with CoPilot, I've added more notes and edited the text.

