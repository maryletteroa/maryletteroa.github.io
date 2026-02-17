---
layout: post
title: Local Modern Data Stack Implementation
categories: [project]
tags: [data-engineering]
image:
    path: /assets/images/local-mds/books_dagster.png
---

I tried implementing a simple local modern data stack (MDS) using the following tools:

- **Duckdb** as database
- **dbt** as transformation and data quality tool
- **Dagster** as scheduler
- **Streamlit** as visualizer

The data is from the [Open Library API](https://openlibrary.org/developers/api).


<center><img src="/assets/images/local-mds/books_dagster.png" alt="model" width="500"/></center>

The Github repository is here: [books-etl](https://github.com/maryletteroa/books-etl)