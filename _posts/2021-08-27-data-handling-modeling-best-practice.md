---
layout: post
title: Data Handling and Data Modeling Best Practice
categories:
- blog
---
Reference: [Microsoft Power BI Desktop for Business Intelligence ](https://www.udemy.com/course/microsoft-power-bi-up-running-with-power-bi-desktop/)

Connecting and Shaping Data
1. Get yourself organized, before loading the data into Power BI
- Define clear and intuitive names (no spaces!) from the start; updating them later can be a headache, specially if you've referenced them in multiple places
- Establish a file/folder structure that makes sense from the start, to avoid having to modify data source settings if file names or locations changes
2. Disabling report refresh for any static sources
- There's no need to constantly refresh sources that don't update frequently (or at all), like lookups or static data tables; only enable refresh for tables that will be changing
3. When working with large table, only load the data you need
- Don't include hourly data when you only need daily, or product-level transactions when you only care about store-level performances; extra data will only slow you down

Creating Relationships and Data Models

4. Focus on building a normalized model from the start
- Make sure that each table in your model serves a single, distinct purpose
- Use relationships vs. merged tables; long & narrow tables are better than short & wide
5. Organize lookup tables above data tables in the diagram view
- This serves as a visual reminder that filters flow "downstream"
6. Avoid complex cross-filtering unless absolutely necessary
- Don't use two-way filters when 1-way filters will get the job done
7. Hide fields from report view to prevent invalid filter context
- Recommend hiding foreign keys from data tables, so that users can only access valid fields

And more! Keep posted!