---
layout: post
title: Ways to write better Python codes
categories:
- blog
---

Source: [11 Tips And Tricks To Write Better Python Code](https://www.youtube.com/watch?v=8OKTAedgFYg)

#### 1. Iterate with `enumerate` instead of `range(len(x))`
```python
data = [1, 2, -4 , -3]
for i, num in enumerate(data):
	if num < 0:
		data[i] = 0
print(data)
	# [1, 2, 0, 0] 
```

#### 2. Use list comprehension instead of raw for loop
```python
squares = [i*i for i in range(10)]
```

#### 3. Sort complex iterables with `sorted()`
List
```python
data = [3, 5, 1, 10, 9]
sorted_data = sorted(data, reverse=True)
print(sorted_data)
	# [10, 9, 5, 3, 1]
```
Dictionary
```python
data = [ {"name": "Max", "age": 6},
	{"name": "Lisa", "age": 20},
	{"name": "Ben", "age": 9},]
sorted_data = sorted(data, key=lambda x: x["age"])
	# key is a function

print(sorted_data)
	# [{"name": "Max", "age": 6}, {"name": "Ben", "age": 9}, {"name": "Lisa", "age": 20}]
```

#### 4. Store unique values with Sets
A set is an unordered collection data type with no duplicate elements.
```python
my_list = {1, 3, 4, 5, 6, 7, 7, 7}
my_set = set(my_list)
print(my_set) 
	# {1, 2, 3, 4, 5, 6, 7}
```

#### 5. Save memory with generators
Generator computes elements lazily, producing one element at a time and only when asked for it
```python
import sys
my_list = [i for i in range(10000)]
print(sum(my_list))
	# 49995000
print(sys.getsizeof(my_list), "bytes")
	# 87632 bytes

my_gen = (i for i in range(10000))
print(sum(my_gen))
	# 49995000
print(sys.getsizeof(my_gen), "bytes")
	# 128 bytes
```

#### 6. Define default values in Dictionaries with `.get()` and `.setdefault()`

```python
my_dict = {"item": "football", "price": 10.00}
count = my_dict["count"]
	# KeyError: 'count'

count = my_dict.get("count")
print(count)
	# None

# with default value
count = my_dict.get("count", 0)
print(count)
	# 0

count = my_dict.setdefault("count", 0)
print(count)
	# 0
print(my_dict)
	# {"item": "football", "price": 10.00, "count": 0}
```

#### 7. Count hashable objects with `collections.Counter`
```python
from collections import Counter

my_list = [10, 10, 10, 5, 5, 2, 9, 9, 9, 9, 9, 9]
counter = Counter(my_list)

print(counter)
	# Counter({9:6, 10: 3, 5:2, 2: 1})

print(counter[10])
	# 3

print(counter[11])
	# 0

most_common = counter.most_common(1)
print(most_common)
	# [(9, 6)]
most_common = counter.most_common(2)
print(most_common)
	# [(10, 3)]
```

#### 8. Format Strings with `f-Strings` (3.6+)
```python
name = "Alex"
my_string = f"Hello {name}"
print(my_string)

# with experssions
i = 10
print(f"{i} squared is {i+1}") 
```

#### 9. Concatenate strings with `.join`
```python
list_of_strings = ["Hello", "my", "friend"]

# BAD!
my_string = ""
for i in list_of_strings:
	my_string += i + " "
# string is immutable so we're creating a new string everytime
# and will be slow for large lists
print(my_string)
	# Hello my friend

# GOOD
my_string = " ".join(list_of_strings)
print(my_string)
	# Hello my friend
```

#### 10. Merge dictionaries with `{**d1, **d2}` (3.5+)
```python
d1 = {"name": "Alex", "age": 25}
d2 = {"name": "Alex", "city": "New York"}
merged_dict = {**d1,**d2}
print(merged_dict)
	# {"name": "Alex", "age": 25, "city": "New York"}
```

#### 11. Simplify if-statement with `if x in [a, b, c]` 

instead of checking each item separately
```python
colors = ["red", "green", "blue"]

c = "red"
if c in colors:
	print("is a main color")
```

