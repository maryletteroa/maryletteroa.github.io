---
layout: post
title: Data Handling and Data Modeling Best Practice
categories:
- blog
---

Reference: [Microsoft Power BI Desktop for Business Intelligence ](https://www.udemy.com/course/microsoft-power-bi-up-running-with-power-bi-desktop/)

The following are lifted from materials in the Udemy Course above 👆. I found this course really helpful in covering the basics of working with PowerBI. Of course, practice and experience are also vital as new features in this software are frequently rolled out.  Since there are plenty of nuances in PowerBI, it's important to keep some sort of best practice guidelines in mind, specially as data and developments scale.

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

Calculated Columns & Measures

8. Don't use a calculated column when a measure will do the trick
- Only use calculated columns to "stamp" static, fixed values to each row in a table
- Use measures when aggregation is necessary, or to create dynamic values in a report
9. Write measures for even the simplest calculations (i.e. Sum of Sales)
- Once you create a measure it can be used to anywhere in the report and as an input to other, more complex calculations (no implicit measures)
10. Break measures down into simple, component parts
- DAX is a difficult language to master; focus on practicing and understanding simple components at first, then assemble them into more advanced formulas
11. Reference columns with the table name, and measure alone
- Using "fully qualified" column references (preceeded by the table name)hepls mae formulas more readanble and intuitive, and differentiates them from measure references

Speed and Peformance

12. Eliminate redundat columns; keep data tables narrow
- Data tables should ideally only contain only quantitative values and foreign keys; any extra descriptive columns can usually live in a related lookup table
13. Imported columns are better than calculated columns
- When possible, create calculated columns at the source (i.e. in your raw database) or within the Query Editor; this is more efficient than processing those calculations in the Data Model
14. Minimize iterator functions (FILTER, SUMX, etc.)
- Functions that cycle through each row in a tabe are "expensive", meaning that they take time and consume processing power


And more! Still not done.