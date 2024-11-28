---
layout: post
title: Cumulative Table
categories: [blog]
tags: [data-engineering, cummulative-table, data, data-modelling, postgres, sql]
---

I've recently learned about [Cumulative tables](https://github.com/DataExpert-io/cumulative-table-design) which is a powerful table design to do historical tracking. The timeframe (however it is defined), are "accumulated" at certain time-partitions, which eliminates the need to do group by or even sorting. This is very useful for tracking states in a dimensional table.

Here's a code snippet of how it's set up. I also learned that PostgresSQL can natively create and handle complex types such as arrays and enums.


Set up tables

```sql
 create type records as (
	col2 text,
	col3 integer,
	col4 real,
	year integer
)

create type class as enum(
	'star', 'good', 'average', 'bad'
)


create table cumulative_table (
	id  text,
	name text,
	arr records[],
	class class ,
	is_active boolean,
	current_year integer,
	primary key (id, current_year)
)

```

Populate cumulative table. `table1` is the source table

```sql

do $$
declare y1 int := (select min(year) from table1);
		y2 int := (select max(year) + 1 from table1);
		y int := 0;


begin
	for y in y1..y2 loop 

insert into cumulative_table

with agg as (
select id
	, name
	, array_agg(row(col2, col3, col4, year)::records) as records
	, (case when avg(col4) > 8 then 'star'
		when avg(col4) > 7 then 'good'
		when avg(col4) > 6 then 'average'
		else 'bad' end)::class  as class 
	, year 
from table1
group by id, name, year 

)

, last_year as (
	select * from cumulative_table
		where current_year = y-1
		
	)

,this_year as (
	select id 
		, name 
		, arr 
		, class
		, year
	from agg
	where year = y

)


	select
		coalesce(t.id, l.id) as id
		, coalesce(t.name, l.name) as name
		, case when l.arr is null
			then t.records
			when t.year is not null then l.records || t.records
			else l.records end as records
		, case when t.year is not null then t.class
			else l.class end as class 
		, case when t.year is not null then true else false end as is_active
		, coalesce(t.year, l.current_year + 1) as current_year
		
	from last_year l
	full outer join this_year t
	on l.id = t.id;

end loop;
end;
$$

```

