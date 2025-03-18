---
layout: post
title: Python collections module
categories: [learning-log]
tags: [python]
---

This is an extension of my [2025 Learning Log]({% link _posts/2025-01-24-2025-learning-log.md %}). 

> Python [collections](https://docs.python.org/3/library/collections.html#module-collections) module contains specialized container datatypes that provide alternatives to Python’s general purpose built-in containers: dict, list, set, and tuple.

### namedtuple

```python
from collections import namedtuple

FullName = namedtuple("FullName", ("first", "middle", "last"))
my_name = FullName("Barney", "The", "Dinosaur")

print(my_name[0]) # Barney
print(my_name.first) # Barney
print(my_name.first) = "Garfield" # AttributeError: can't set attribute
# namedtuples are read-only
```

### deque
- lists with fixed maximum length (optional)
- double-sided limited lists

```python
from collections import deque

numbers = deque([], maxlen=5)

# first in, first out
for i in range(10):
	numbers.append(i)
	print(numbers)

"""
deque([0], maxlen=5)
deque([0, 1], maxlen=5)
deque([0, 1, 2], maxlen=5)
deque([0, 1, 2, 3], maxlen=5)
deque([0, 1, 2, 3, 4], maxlen=5)
deque([1, 2, 3, 4, 5], maxlen=5)
deque([2, 3, 4, 5, 6], maxlen=5)
deque([3, 4, 5, 6, 7], maxlen=5)
deque([4, 5, 6, 7, 8], maxlen=5)
deque([5, 6, 7, 8, 9], maxlen=5)
"""

numbers.appendleft(4)
print(numbers) # deque([4, 5, 6, 7, 8], maxlen=5)

n = numbers.popleft()
print(n) # 4 
```


### defaultdict

```python
from collections import defaultdict

# default element is an empty list
items = defaultdict(list)
items["Ethan"].append("views")
print(items) # defaultdict(<class 'list'>, {'Ethan': ['views']})

items = defaultdict(int)
items["Ethan"] += 1
print(items) # defaultdict(<class 'int'>, {'Ethan': 1})

items = defaultdict(lambda: 7)
items["Ethan"] += 1
print(items) # defaultdict(<function <lambda> at 0x103043d80>, {'Ethan': 8})

```

### Counter
Counter - container that stores the elements as dictionary keys and their counts as dictionary values

```python
from collections import Counter
a = "aaaaabbbbccc"
my_counter = Counter(a)
print(my_counter) # Counter({'a': 5, 'b': 4, 'c': 3})
print(my_counter.most_common(1)) # [('a', 5)]
print(my_counter.most_common(2 # [('a', 5), ('b', 4)]
print(my_counter.most_common(1)[0][0]) # a
print(list(my_counter.elements())) # ['a', 'a', 'a', 'a', 'a', 'b', 'b', 'b', 'b', 'c', 'c', 'c']
```

### OrderedDict
Remembers the order that the items were inserted. This is guaranteed already in Python 3.7 so `OrderedDict` are useful when using older Python versions

```python
from collections import OrderedDict
ordered_dict = OrderedDict()
ordered_dict["b"] = 2
ordered_dict["c"] = 3
ordered_dict["d"] = 4
ordered_dict["a"] = 1
print(ordered_dict) # OrderedDict({'b': 2, 'c': 3, 'd': 4, 'a': 1})
```


## Resources
- [The Python collections module is OVERPOWERED](https://www.youtube.com/watch?v=pn0QnQv1Q8w)
- [Collections in Python- Advanced Python 06 - Programming Tutorial](https://www.youtube.com/watch?v=UdcPhnNjSEw&t=3s)
- [Python's collections: A Buffet of Specialized Data Types](https://realpython.com/python-collections-module/)