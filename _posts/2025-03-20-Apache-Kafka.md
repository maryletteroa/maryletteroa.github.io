---
layout: post
title: Apache Kafka
categories: [learning-log]
tags: [kafka]
---

This is an extension of my [2025 Learning Log]({% link _posts/2025-01-24-2025-learning-log.md %}). 

> ⚠️ This post is currently a work-in-progress as I am still going through the materials

I started learning Apache Kafka. I wanted to study Flink actually but since it comes downstream of Kafka, I figured I might as well learn a bit more about Kafka first.

I am learning through this course [The Complete Apache Kafka Practical Guide](https://www.udemy.com/course/apache_kafka/). The version used in the videos is a bit older and still uses [Zookeeper](https://zookeeper.apache.org/). So I'm going back and forth between this course and other materials I find in the [official docs](https://kafka.apache.org), the interwebs, and/or YouTube.

Kafka has [been moving away from using Zookeeper](https://www.baeldung.com/kafka-shift-from-zookeeper-to-kraft) and has introduced the KRaft protocol (Kafka Raft Metadata mode). This eliminates the need for Zookeeper, making Kafka simpler to deploy and manage.

## Introduction

Here is an [introduction to Kafka](https://kafka.apache.org/intro) from the [official docs](https://kafka.apache.org).

event 
- an indication in time that the thing took place
- e.g. represents a thing that happened in the business
- stored in topics

log
- structure that stores events (events are not stored in databases)
- ordered sequence of events
- easy to build at scale, easier than databases

Apache Kafka 
- is a system for managing these logs
- think of events first, things second


topics 
- ordered sequence of events stored in a durable way (stored in disc, replicated)
- can store topics for short or long time
- topics can be small or enormous


Programs can talk to each other through Kafka topic. Each program consumes a message from a Kafka topic, do computations (e.g. grouping, filtering, enriching the data from another topic), then produce that message into another separate Kafka topic to be likewise durably stored and processed - e.g. by a new service that perform real-time analysis of the data


[Kafka connect](https://kafka.apache.org/documentation/#connect)
- enables Kafka to connect with other systems using connectors

[Kafka streams](https://kafka.apache.org/documentation/streams/)
- API that handles all framework and infrastructure to process data in Kafka in a scalable and fault-tolerant way


## Installation
There are two ways to [install Kafka](https://kafka.apache.org/quickstart) - using the binary, and from docker.  Using Docker is fairly straight-forward, and no need to manually install or manage a compatible Java version. I tried the steps in this [article](https://developer.confluent.io/confluent-tutorials/kafka-on-docker/) which uses a docker compose file.

I also tried using the binary, which requires a prior installation of Java version 17 and up. My machine defaults to version 11 so had to spend some time linking the approriate version which already exists (in my case version 23).

Here's the rough steps.

Install and unpack

```bash
curl https://dlcdn.apache.org/kafka/4.0.0/kafka_2.13-4.0.0.tgz -o ~/Downloads/kafka.tgz

mkdir kafka
cd kafka
tar -xvzf ~/Downloads/kafka.tgz --strip 1
```

Install Java

```bash
# check java version or if java is present 
java -version

# to install
# use apt install
sudo apt install openjdk-11-jdk
# or use brew install
brew install openjdk@23

```

For existing installation, make sure it's the one being linked when calling the Java binary from the terminal: I used this [Stack overflow](https://stackoverflow.com/questions/69875335/macos-how-to-install-java-17) troubleshooting as reference


```bash

sudo ln -sfn /opt/homebrew/opt/openjdk\@23/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk.jdk

export JAVA_HOME=`/usr/libexec/java_home -v 23`

echo 'export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"' >> ~/.zshrc

source ~/.zshrc

java -version
```

Then I followed the rest of the steps in the [installation/ quick start docs](https://kafka.apache.org/quickstart) 

Generate a Cluster UUID

```bash
$ KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
```

Format Log Directories

```bash
$ bin/kafka-storage.sh format --standalone -t $KAFKA_CLUSTER_ID -c config/server.properties
```

Start the Kafka Server

```bash
$ bin/kafka-server-start.sh config/server.properties
```


## Creating a Kafka topic

Use the binaries located in the installation folder e.g. `/opt/kafka/bin`

```bash
./kafka-topics.sh --create --bootstrap-server localhost:9092 --topic cities
```

list topics

```bash
./kafka-topics.sh --list --bootstrap-server localhost:9092
```

details of the topic

```bash
./kafka-topics.sh --describe --bootstrap-server localhost:9092
```

output

```text
Topic: cities   TopicId: aQjPyaLhTU-Toc1VxCugYw PartitionCount: 1 ReplicationFactor: 1    Configs: 
        Topic: cities   Partition: 0    Leader: 1Replicas: 1      Isr: 1  Elr:    LastKnownElr: 
```

`ReplicationFactor=1` - only one server will save the topics

delete a topic

```bash
./kafka-topics.sh --delete --topic my-topic --bootstrap-server localhost:9092
```

## Producing and consuming messages
`kafka-console-producer.sh` - producer that ships with kafka
- used to send messages to topics

```bash
./kafka-console-producer.sh  --topic cities --bootstrap-server localhost:9092
```
enter names of cities

```text
>New York
>Berlin
>Paris
>London
>Sydney
```

Open another terminal. Use the built in consumer

```bash
./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic cities
```

add `Delhi` in producer, consumer should return `Delhi`  
add `Dubai` in producer, consumer should return `Dubai`

`--from-beginning` flag -- will show the earlier cities including the two newly added

```bash
./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic cities --from-beginning
```

results

```text
New York
Berlin
Paris
London
Sydney
Delhi
Dubai
```

> Apache Kafka cluster store messages even if they were already consumed by one of the consumers. Same messages maybe read multiple times by different consumers at different moments of time

### Run multiple consumers
launch another consumer, add `Amsterdam` in producer, should show both `Amsterdam` in the two producers

> Multiple consumers and multiple producers could exchange messages via single centralized storage point - Kafka cluster

### Run multiple producers
launch a new producer and write `Barcelona`  
consumer 1 and consumer 2 should also show `Barcelona`

> Producers and consumers don't know about each other. Producers and consumers may appear and disappear. But Kafka doesn't care about that. It's job is to store messages and receive or send them on demand.

Stopping one of the producers will not affect the rest. Likewise, stopping a consumer will not affect the others.

## Where does Kafka store messages

Find the log path in the `server.properties` file
```bash
cat /opt/kafka/config/server.properties
```

```text
...
log.dirs=/tmp/kraft-combined-logs
```

```bash
cd /tmp/kraft-combined-logs
```

would have 50 folders of `__consumer_offsets-<number>` from 0-49
- these are 50 partitions by system topic called `__consumer_offsets`

`cities-0`
- single partition only of the defined topic


```bash
cd cities-0/
ls
cat 00000000000000000000.log
```

Kafka stores messages in the `*.log` file as text


> Kafka doesn't store all messages forever and after specific amount of time (or when size of the log exceeds configured max size) messages are deleted.

Default log retention period is 7 days (168 hours)


Logs `/opt/kafka/logs/server.log.2025-03-24-11`

Partitions are spread among all available brokers

> Every consumer must belong to a consumer group.

> Every message inside the topic has unique number called "offset". First message in each topic has offset 0. Consumers start reading messages starting from specific offset


```text
mesagge -------- Offsets
>New York -------- 0
>Berlin ---------- 0
>Paris ----------- 0
>London ---------- 0
>Sydney ---------- 0
```
