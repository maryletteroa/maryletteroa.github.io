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
