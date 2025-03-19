---
layout: post
title: Python logging using loguru
categories: [learning-log]
tags: [python]
---

This is an extension of my [2025 Learning Log]({% link _posts/2025-01-24-2025-learning-log.md %}). 

## About
Loguru is a python package for logging. It is intended to make logging simpler, less painful, and enjoyable. 

## Installation

`pip install loguru`

## Log levels
There are seven log levels in loguru. Each of the log level is associated with a numerical value, and a constant name. The default level is `DEBUG`. 

- `TRACE` (5): record fine-grained information about the program's execution path for diagnostic purposes
- `DEBUG` (10): record messages for debugging purposes
- `INFO` (20): record informational messages that describe the normal operation of the program
- `SUCCESS` (25): similar to `INFO` but used to indicate the success of an operation
- `WARNING` (30): indicate an unusual event that may require further investigation
- `ERROR` (40): record error conditions that affected a specific operation.
- `CRITICAL` (50): record error conditions that prevent a core function from working

```python
...
logger.trace("A trace message.")
logger.debug("A debug message.")
logger.info("An info message.")
logger.success("A success message.")
logger.warning("A warning message.")
logger.error("An error message.")
logger.critical("A critical message.")
```

Output

```text
2022-08-10 11:58:33.224 | DEBUG | __main__:<module>:12 - A debug message.
2022-08-10 11:58:33.224 | INFO | __main__:<module>:13 - An info message.
2022-08-10 11:58:33.225 | SUCCESS | __main__:<module>:14 - A success message.
2022-08-10 11:58:33.226 | WARNING | __main__:<module>:15 - A warning message.
2022-08-10 11:58:33.226 | ERROR | __main__:<module>:16 - An error message.
2022-08-10 11:58:33.227 | CRITICAL | __main__:<module>:17 - A critical message.

```

Aside from these, custom log levels can also be defined.

```python
import sys
from loguru import logger

logger.level("FATAL", no=60, color="<red>", icon="!!!")
logger.log("FATAL", "A user updated some information.")

```

Output

```text
2022-08-26 11:34:13.971 | FATAL   | __main__:<module>:42 - A user updated some information.
```

## Contextual data

Contextual data include other relevant information that may be useful for filtering, correlating, or tracing information in the logs

In loguru, these are contained within the `{extract}` directive

```python
logger.add(sys.stderr, format="{time:MMMM D, YYYY > HH:mm:ss} | {level} | {message} | {extra}")

```

Either `bind()` or `contextualize` can be used to log contextual information

Using `bind()` creates a child logger that inherits contextual data from its parent. It does not affect the original `logger`

```python
import sys
from loguru import logger

logger.remove(0)
logger.add(sys.stderr, format="{time:MMMM D, YYYY > HH:mm:ss} | {level} | {message} | {extra}")

childLogger = logger.bind(seller_id="001", product_id="123")
childLogger.info("product page opened")
childLogger.info("product updated")
childLogger.info("product page closed")

logger.info("INFO message")

```

Output

```text
September 16, 2022 > 13:04:10 | INFO | product page opened | {'seller_id': '001', 'product_id': '123'}
September 16, 2022 > 13:04:10 | INFO | product updated | {'seller_id': '001', 'product_id': '123'}
September 16, 2022 > 13:04:10 | INFO | product page closed | {'seller_id': '001', 'product_id': '123'}
September 16, 2022 > 13:06:08 | INFO | INFO message | {}
```

Using `contextualize()` method modifies `extra` directly and does not return a new `logger`. It needs to be used with a `with` statement


```python
import sys
from loguru import logger

logger.remove(0)
logger.add(sys.stderr, format="{time:MMMM D, YYYY > HH:mm:ss} | {level} | {message} | {extra}")

def log():
    logger.info("A user requested a service.")


with logger.contextualize(seller_id="001", product_id="123"):
    log()

```

Output

```text
August 12, 2022 > 11:00:52 | INFO | A user requested a service. | {'seller_id': '001', 'product_id': '123'}
```

## Example usage

```python
import sys
from loguru import logger

# remove default configuration
logger.remove()

# create a handler that has a custom format
# items in curly brances {...} are called directives 
# by default, logs are sent to the sys.stderr
# sys.stdout outputs to terminal
# <level> directive uses different colors for different levels
	# can also use colors e.g. <green>
logger.add(
	sys.stdout, 
	format = "{time:MMMM D, YYYY} {level} --- <level>{message}</level> {extra}",
	serialize = True, # outputs log in JSON
	level = "WARNING" # any level below this will not be outputted
)

# possible to setup more than one handlers
logger.add(
	"app.log" # output log to file,
	serialize = True,
	rotation = "5 seconds", # sends logs to a new log file once previous log file has expired; can also be in terms of file size e.g. "1 MB"
	retention = "10 seconds", # keeps only recent log files, deletes expired log files (compressed or uncompressed) generated more than 10 seconds ago
    compression = "zip" # expired logs are compressed

# ------------ #
## add contextual data
# can pass as many key-values as you want
child_logger = logger.bind(user_id = 1, ip_adress = "192.158.1.38")
# these will now contain the {extra} dictionary
child_logger.info("An info message!!!")
child_logger.error("An error occured!!!")

# using contextualize() instead of bind()
# needs to be inside the with context manager
with logger.contextualize(user_id = 1, ip_adress = "192.158.1.38"):
	logger.info("An info message!!!")
	logger.error("An error occured!!!")

# ------------ #
## logging error
# using a decorator
@logger.catch(level = "CRITICAL") # default is level ERROR
def read_file(filename):
	with open(filename) as f:
		return f.read()

# alternatively, use a context manager
with logger.catch():
	read_file("input.txt") # this file does not exist

```

## Structured logging

Loguru can output structured logs in the form of JSON using the parameter `serialize = True` in `logger.add()`.

The default output can be further customized as in the example below using `logger.patch()`

```python
import sys
import json
from loguru import logger


def serialize(record):
    subset = {
        "timestamp": record["time"].timestamp(),
        "message": record["message"],
        "level": record["level"].name,
    }
    return json.dumps(subset)


def patching(record):
    record["extra"]["serialized"] = serialize(record)


logger.remove(0)

logger = logger.patch(patching)
logger.add(sys.stderr, format="{extra[serialized]}")
logger.debug("Happy logging with Loguru!")

```

Output

```text
{"timestamp": 1663328693.765488, "message": "Happy logging with Loguru!", "level": "DEBUG"}
```

## Some best practice

As logging can affect the performance of an application, it is important to be mindful of how much and how often logging is used. It should be enough to enable diagnosing potential issues but not impact the application performance.

Rotate log files periodically to manage log file size, avoid performance issues, and simplify debugging. Rotating log files means periodically creating new log file, archiving or deleting old ones.

Write meaningful log messages. These include
- Being clear and concise - be on point and avoid jargon
- Providing context - e.g. what function generated the info, what are the input parameters
- Consistency - use a consistent format across log messages
- Providing actionable insights (e.g. how to resolve the issue, or link to relevant documentation)

Keep sensitive data out of log files. 

## Resources
- [Github Loguru](https://github.com/Delgan/loguru)
- [Docs](https://loguru.readthedocs.io/en/stable/overview.html)
- [Loguru - Simplified Python Logging with Loguru](https://www.youtube.com/watch?v=gSc1oHcwkE4&t=1504s)
- Better Stack 
	- [Better Stack observability platform](https://betterstack.com/)
	- [A Complete Guide to Logging in Python with Loguru](https://betterstack.com/community/guides/logging/loguru/)
	- [10 Best Practices for Logging in Python](https://betterstack.com/community/guides/logging/python/python-logging-best-practices/)
	- [15 Common Errors in Python and How to Fix Them](https://betterstack.com/community/guides/scaling-python/python-errors/)