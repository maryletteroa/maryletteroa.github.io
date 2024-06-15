---
layout: post
title: Power Query Calendar Table
categories:
- blog
---

Here's a Power Query snippet to create a Calendar in Power BI

In the Power Query Editor:

1. Create a Calendar table with one column [StartDate] containing the starting date of the calendar e.g. 2017-01-01.  
    - To create a new table, click on Home > Enter Data
2. Right click the Calendar table, click "Advance Editor"
3. Paste the following code from #"Change Type" step. (The first step "Source" should refer to the table created in step 1)


```
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMjIwMtY1MAQipdhYAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [StartDate = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{ {"StartDate", type date}}),
    #"Added Custom" = Table.AddColumn(#"Changed Type", "EndDate", each Date.From(DateTime.LocalNow())),
    #"Changed Type1" = Table.TransformColumnTypes(#"Added Custom",{ {"EndDate", type date}}),
    #"Added Custom1" = Table.AddColumn(#"Changed Type1", "Date", each {Number.From([StartDate])..Number.From([EndDate])}),
    #"Expanded Date" = Table.ExpandListColumn(#"Added Custom1", "Date"),
    #"Changed Type2" = Table.TransformColumnTypes(#"Expanded Date",{ {"Date", type date}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type2",{"StartDate", "EndDate"}),
    #"Added Custom2" = Table.AddColumn(#"Removed Columns", "Year", each Date.Year([Date])),
    #"Added Custom3" = Table.AddColumn(#"Added Custom2", "Month", each Date.Month([Date])),
    #"Added Custom4" = Table.AddColumn(#"Added Custom3", "Month_Name", each Date.MonthName([Date])),
    #"Added Custom5" = Table.AddColumn(#"Added Custom4", "Month_Name_Short", each Text.Start([Month_Name],3)),
    #"Added Custom6" = Table.AddColumn(#"Added Custom5", "Period", each Text.From( [Year] ) & "-" & Text.End( "0" & Text.From ( [Month] ), 2 )),
    #"Changed Type3" = Table.TransformColumnTypes(#"Added Custom6",{ {"Year", Int64.Type}, {"Month", Int64.Type}})
in
    #"Changed Type3"

```

The end date is dynamic and would be set to the current date each refresh.

This would result in the following Calendar Table

- Date: date - 1/1/2017
- Year: int - 2017
- Month: int - 1
- Month_Name: str - January
- Month_Name_Short: str - Jan
- Period: str - 2017-01

<center><img src="/assets/images/power-query-calendar-table.png" alt="power-query-calendar-table" width="800"/></center>

