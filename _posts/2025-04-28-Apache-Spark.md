---
layout: post
title: Apache Spark
categories: [learning-log]
tags: [spark, pyspark]
mermaid: true
---

This is an extension of my [2025 Learning Log]({% link _posts/2025-01-24-2025-learning-log.md %}).

Reviewing Spark (PySpark) through this course [Taming Big Data With Apache Spark](https://www.udemy.com/course/taming-big-data-with-apache-spark-hands-on/)

## Setting up

Apache Spark 3.x is only compatible with Java 8, Java 11, or Java 17, and Apache Spark 4 is only compatible with Java 17.

Currently, Spark is not compatible with Python 3.12 or newer.

So I needed to install alternative lower versions of Java and Python.

Install Java 11

```bash
brew install openjdk@11
```

Make sure that it is the default Java in the system

```bash
cd /Library/Java/JavaVirtualMachines/jdk-23.jdk/Contents
mv Info.plist Info.plist.disabled

sudo ln -sfn /opt/homebrew/opt/openjdk\@11/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk.jdk
export JAVA_HOME=`/usr/libexec/java_home -v 11`
java -version
```

Downgrade Python

```bash
brew install python@3.10
```

Create a virtual environment

```bash
python3.10 -m pip3 install virtualenv
python3.10 -m virtualenv .venv
source .venv/bin/activate

# test
pyspark
```

To test 

```bash
spark-submit test.py
```

## Spark 3.5 and Spark 4 features

Here are some of the new features in Spark 3.5 or Spark 4

- Spark Connect
    - Client / Server architecture for Apache Spark
	- allows control of remote cluster
- Expanded SQL functionality
    - e.g. UDTF's, optimized UDFs, more SQL functions
- English SDK
    - e.g.

```python
transformed_df = revenue_df.ai.transform('What are the best-selling and the second best-selling products in every category')
```

- Debugging features 
    - e.g. enhanced error messages, testing API
- DeepSpeed Distributor
    - distributed training for PyTorch models
- ANSI mode by default
    - i.e. better error handling in SQL-style queries
- Variant Data type
    - better support for semi-structured data
- Collation support
    - for sorting and comparisons e.g. case sensitivity, unicode-support
- Data source APIs (Python)
    - read or write to custom data sources or sinks, respectively
- RDD interface at legacy, instead DataFrame API is emphasized
- Delta Lake 4.0 support

## Introduction to Spark

Spark is a fast and general engine for large-scale data processing.

It is characterized by its scalability and fault-tolerance features.

Lazy evalution - it doesn't do anything until it is asked to produce results; creates DAGs (direct acyclic graph) of steps to produce said results, and figures out the optimal path; reason why Spark is fast

Components of Spark

- Spark core

    - Spark streaming
    - Spark SQL
    - MLLib
    - GraphX

## Introduction to RDDs

RDD is Spark's original dataset structure - under the hood, it is the core object that everything in Spark revolves around

Dataset - abstraction for a giant set of data
Distributed - distribute processing of data; spread out across clusters of computer; may or may not be local
Resilient - handle failures, redistribute load when failure occurs

Use the RDD object to do actions on the dataset

Spark Context - responsible for making RDDs resilient and distributed

## Filtering RDDs

snippet
- `.filter()`
- `.reduceByKey`

```python
# minimum temperature
minTemps = parsedLines.filter(lambda x: "TMIN" in x[1])
stationTemps = minTemps.map(lambda x: (x[0], x[2]))
minTemps = stationTemps.reduceByKey(lambda x, y: min(x, y))
results = minTemps.collect()

# max temperature

lines = sc.textFile("data/1800.csv")
parsedLines = lines.map(parseLine)
maxTemps = parsedLines.filter(lambda x: "TMAX" in x[1])
stationTemps = maxTemps.map(lambda x: (x[0], x[2]))
maxTemps = stationTemps.reduceByKey(lambda x, y: max(x, y))
results = maxTemps.collect()
```

## Map vs Flatmap

`map()` - transforms each element of an RDD to one new element; i.e. 1:1
`flatmap()` - can create many new elements from each


```python
# flat map and countByValue()
words = input.flatMap(lambda x: x.split())
wordCounts = words.countByValue()

# using Regex
def normalizeWords(text):
    return re.compile(r"\W+", re.UNICODE).split(text.lower())
...
words = input.flatMap(normalizeWords)

# sorting using sortByKey()
words = input.flatMap(normalizeWords)
wordCounts = words.map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y)
wordCountsSorted = wordCounts.map(lambda x: (x[1], x[0])).sortByKey()
```

## Spark SQL
RDD's can be extended to Dataframe objects

Dataframe
- trend in Spark is to use RDD's less, and dataframes more
- contains row objects
- can run SQL queries
- can have a schema (leads to efficient storage)
- can read and write to JSON, Hive, parquet, csv etc file formats
- communicates with JDBC/ODBC, Tableau
- allows for better interoperability
    - MLLib and Spark Streaming are moving towards using dataframes instead of RDD's for their primary API
- simplifies development
    - can just perform SQL operations on a dataframe with one line
- can also set up Shell access


Dataframes vs Datasets
- In Spark 2+, a DataFrame is really a DataSet of Row objects
- Not very relevant in Python as it is untyped, but in Scala, use Datasets whenever possible
    - because they are typed, they can be stored more efficiently
    - can also be optimized at compile time

Using Spark SQL in Python

```python
from pyspark.sql import SparkSession, Row

spark = SparkSession.builder.appName("SparkSQL").getOrCreate()

inputData = spark.read.json(dataFile)
inputData.createOrReplaceTempView("myStructuredStuff")

myResultDataFrame = spark.sql("SELECT food from bar ORDER BY foobar")
```

Alternatively, methods can be used instead of SQL statements

```python
myResultDataFrame.show()
myResultDataFrame.select("someFieldName")
myResultDataFrame.filter(myResultDataFrame("someFieldName" > 200))
myResultDataFrame.groupBy(myResultDataFrame("someFieldName")).mean()

#convert dataframe to RDD
myResultDataFrame.rdd().map(mapperFunction)
```

User-defined functions (UDF's)

```python
from pyspark.sql.types import IntegerType

def square(x):
    return x*x

spark.udf.register("square", square, IntegerType())
df = spark.sql("SELECT square('someNumericField') FROM tableName")
```

Data without a header

```python
from pyspark.sql import Row, SparkSession

# Create a SparkSession
spark = SparkSession.builder.appName("SparkSQL").getOrCreate()


def mapper(line):
    fields = line.split(",")
    return Row(
        ID=int(fields[0]),
        name=str(fields[1].encode("utf-8")),
        age=int(fields[2]),
        numFriends=int(fields[3]),
    )


lines = spark.sparkContext.textFile("data/fakefriends.csv")
people = lines.map(mapper)

# Infer the schema, and register the DataFrame as a table.
schemaPeople = spark.createDataFrame(people).cache()
schemaPeople.createOrReplaceTempView("people")
```

Data with header, and using infer schema

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("SparkSQL").getOrCreate()

people = (
    spark.read.option("header", "true")
    .option("inferSchema", "true")
    .csv("data/fakefriends-header.csv")
)

print("Here is our inferred schema:")
people.printSchema()
```

Aggregate, sort, alias 

```python
friendsByAge.groupBy("age").agg(func.round(func.avg("friends"), 2).alias("friends_avg")).sort("age").show()
```

Unstructured data

`func.explode()` - similar to flatmap; explodes columns into rows

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as func

spark = SparkSession.builder.appName("WordCount").getOrCreate()

# Read each line of my book into a dataframe
inputDF = spark.read.text("data/book.txt")

# Split using a regular expression that extracts words
words = inputDF.select(func.explode(func.split(inputDF.value, "\\W+")).alias("word"))
wordsWithoutEmptyString = words.filter(words.word != "")

# Normalize everything to lowercase
lowercaseWords = wordsWithoutEmptyString.select(
    func.lower(wordsWithoutEmptyString.word).alias("word")
)
```

Using custom schema

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as func
from pyspark.sql.types import (
    FloatType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

spark = SparkSession.builder.appName("MinTemperatures").getOrCreate()

schema = StructType(
    [
        StructField("stationID", StringType(), True),
        StructField("date", IntegerType(), True),
        StructField("measure_type", StringType(), True),
        StructField("temperature", FloatType(), True),
    ]
)

# // Read the file as dataframe
df = spark.read.schema(schema).csv("data/1800.csv")
df.printSchema()
```

## Pandas on Spark
- Pandas is often used for prototyping or transforming small data but it doesn't scale well
- Pandas integration in Spark allows scaling up of Pandas up to big data
- Can move DataFrames between Pandas and Spark
- Or apply Pandas-style operations on Spark DataFrames


```python
# Must set this env variable to avoid warnings
import os

from pyspark.sql import SparkSession
import pandas as pd
import pyspark.pandas as ps  # Alias for pandas API on Spark

...

# Create a Pandas DataFrame
pandas_df = pd.DataFrame(
    {
        "id": [1, 2, 3, 4, 5],
        "name": ["Alice", "Bob", "Charlie", "David", "Emma"],
        "age": [25, 30, 35, 40, 45],
    }
)

print("Pandas DataFrame:")
print(pandas_df)

# Convert Pandas DataFrame to Spark DataFrame
spark_df = spark.createDataFrame(pandas_df)

print("\nSchema of Spark DataFrame:")
spark_df.printSchema()

filtered_spark_df = spark_df.filter(spark_df.age > 30)

# Convert Spark DataFrame back to Pandas DataFrame
converted_pandas_df = filtered_spark_df.toPandas()
print("\nConverted Pandas DataFrame:")
print(converted_pandas_df)

# Use pandas-on-Spark for scalable Pandas operations
ps_df = ps.DataFrame(pandas_df)
ps_df["age"] = ps_df["age"] + 1

# Convert pandas-on-Spark DataFrame to Spark DataFrame
converted_spark_df = ps_df.to_spark()
converted_spark_df.show()
```

`DataFrame.transform()`
    - must return same length as input

`DataFrame.apply()`
    - return might be a different length

```python
# Using `transform()` for element-wise operations
ps_df["age_in_10_years"] = ps_df["age"].transform(lambda x: x + 10)

#  Using `apply()` on columns
# Define a custom function to categorize salary levels
def categorize_salary(salary):
    if salary < 60000:
        return "Low"
    elif salary < 100000:
        return "Medium"
    else:
        return "High"


# Apply the function to the 'salary' column
ps_df["salary_category"] = ps_df["salary"].apply(categorize_salary)
```



## UDF and UDFT

UDFs
- User-defined functions
- allow custom logic to be applied row by row in SparkSQL or DataFrame
- one row at a time, each row must be serialized / deserialize
- used when built-in Spark functions are not sufficient

UDTFs
- User-defined table functions
- one input row may return multiple output rows and columns
- Useful for transforming nested or structured data (e.g. expanding JSON, arrays, hierarchical data)
- More efficient on large tables


```python
import re

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, udtf
from pyspark.sql.types import IntegerType

# ----------------------------
# User-Defined Table Function (UDTF)
# ----------------------------
@udtf(returnType="hashtag: string")
class HashtagExtractor:
    def eval(self, text: str):
        """Extracts hashtags from the input text."""
        if text:
            hashtags = re.findall(r"#\w+", text)
            for hashtag in hashtags:
                yield (hashtag,)


# ----------------------------
# User-Defined Function (UDF)
# ----------------------------
@udf(returnType=IntegerType())
def count_hashtags(text: str):
    """Counts the number of hashtags in the input text."""
    if text:
        return len(re.findall(r"#\w+", text))
    return 0

...
# Register the UDTF for use in Spark SQL
spark.udtf.register("extract_hashtags", HashtagExtractor)

# Register the UDF for use in Spark SQL
spark.udf.register("count_hashtags", count_hashtags)

# ----------------------------
# Example: Using the UDTF in SQL
# ----------------------------
print("\nUDTF Example (Extract Hashtags):")
spark.sql(
    "SELECT * FROM extract_hashtags('Welcome to #ApacheSpark and #BigData!')"
).show()

# ----------------------------
# Example: Using the UDF in SQL
# ----------------------------
print("\nUDF Example (Count Hashtags):")
spark.sql(
    "SELECT count_hashtags('Welcome to #ApacheSpark and #BigData!') AS hashtag_count"
).show()

```

## Spark Connect
- Client/Server architecture for Spark
- Dataframes only (does not support RDDs, SparkContext API)
- With Spark Connect, there's no need to run the script in the same server as the Spark Driver
- There's a Spark Connect API that sits in between the app and the Spark driver
- Language agnostic
- Less likely for an application to bring down the whole Spark server
- Apps will also require less memory, and start faster

Example steps

```bash
# install pyspark connect package
pip install pyspark[connect]==4.0.0.dev2

# start spark connect
./sbin/start-connect-server.sh --packages org.apache.spark:spark-connect_2.13:4.0.0-preview2

# run the python script (no need to run spark-submit)
python3 spark_script.py
```

In the Spark script, `SparkSession` is constructed like this

```python
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder.remote("sc://localhost:15002")
    .appName("MovieSimilarities")
    .getOrCreate()
)
```

