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