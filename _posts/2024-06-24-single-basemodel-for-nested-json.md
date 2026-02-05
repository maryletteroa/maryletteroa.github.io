---
layout: post
title: Single BaseModel for nested JSON
categories: [blog]
tags: [python, pydantic]
---

Suppose a dataset looks something like this, with no overlapping keys:

```json
"rows": [
    {
        "a": "1234ABC",
        "b": 5.768,
        "c": 1,
        "d": [
            {
                "e": "GHT5678",
                "f": "F0000123",
                "g": 1
            },
            {
                "e": "GHT5679",
                "f": "F0000124",
                "g": 2
            },
            {
                "e": "GHT5680",
                "f": "F0000125",
                "g": 3
            },
        ]
    }
]
```

A single [`BaseModel`](https://docs.pydantic.dev/latest/api/base_model) can be created


```python

Example(BaseModel):
    a: str
    b: float
    c: int
    e: str
    f: str
    g: int

```

Instead of iterating on each key or defining the parent and child into separate data classes, both can be read as dictionaries, merged, and then unpacked into `Example`:

```python
data = list()
for row in rows:
	for child in row.get("d"):
		_d = {
			**{k: row[k] for k in row if k != "d"},
			**child
		}
		data.append(Example(**_d))
```



Full example:

```python
from pydantic import BaseModel

class Example(BaseModel):
    a: str
    b: float
    c: int
    e: str
    f: str
    g: int



rows = {"rows": [
    {
        "a": "1234ABC",
        "b": 5.768,
        "c": 1,
        "d": [
            {
                "e": "GHT5678",
                "f": "F0000123",
                "g": 1
            },
            {
                "e": "GHT5679",
                "f": "F0000124",
                "g": 2
            },
            {
                "e": "GHT5680",
                "f": "F0000125",
                "g": 3
            },
        ]
    }
] }



data = list()
for row in rows.get("rows"):
	for child in row.get("d"):
		_d = { **{k: row[k] for k in row if k != "d"},
			**child
		}
		data.append(Example(**_d))

print(data)
```