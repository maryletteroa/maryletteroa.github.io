---
layout: post
title: Validate, Correct and Quarantine Data Using Pydantic
categories: [blog]
tags: [python, pydantic, data]
---


Here's a demo on how `pydantic` can be used to validate, correct, and quarantine data.

Access the code and demo file [here](https://github.com/maryletteroa/data_analytics/tree/main/demo/blog/2024-06-29-pydantic-validate-correct-quarantine).

Given a csv file `users.csv` containing the following records
```
id,name,email
1001,ana,ana@example.com
1002,isabel,isabel@example.com
1003,kris,kris@example.com
1004,bee,bee@ example.com
100s,kim,jan@example.com
```
Column `id` is expected to be an integer, `name` is expected to be a string, and `email` is expected to be a valid email address.

The data can be modeled using `pydantic`.

```python
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: int
    name: str
    email: EmailStr
```

[`EmailStr`](https://docs.pydantic.dev/2.3/usage/types/string_types/) is a built-in type in `pydantic` that can be used to validate email addresses. It depends on the library `email-validator` and so this needs to also be installed along with `pydantic`.

```
pip install pydantic
pip install email-validator
```

Running the data through this `BaseModel` will result in two (2) errors: there is an invalid `email` for user `bee`, and an invalid `id` for user `kim`.

The email can be easily corrected by removing the space. To do this, [`model_validator`](https://docs.pydantic.dev/2.3/usage/validators/#model-validators) with `mode=before` can be used. This means, the function to correct the email address will run [first before the the inner validators](https://docs.pydantic.dev/2.3/usage/dataclasses/#initialization-hooks) `int`, `str,` and `EmailStr`.


```python
from pydantic import BaseModel, EmailStr, field_validator, model_validator


class User(BaseModel):
    id: int
    name: str
    email: EmailStr

    @model_validator(mode="before")
    def correct_email(cls, data: dict):
        # remove space in email address
        data["email"] = data["email"].replace(" ", "")
        return data
```

Unlike the incorrect `email`, the erroneous `id` looks less straight-forward to correct, and so it's best to quarantine this row to be handled at a later time. The rest of the passing records can be processed first. 

To do this, the [`ValidationErrors`](https://docs.pydantic.dev/2.3/errors/validation_errors/) Exception in `pydantic` can be set-up to capture and set-aside the records, along with the error details.


```python
# import ValidationError from `pydantic_core`
from pydantic_core import ValidationError


# ...

# define passed and quarantine lists
users_passed = list()
users_quarantined = list()

clines = 0
with open("users.csv") as inf:
    for i, user in enumerate(inf):
        if i != 0:
            clines += 1
            data = user.strip().split(",")
            try:
                user = User(id=data[0], name=data[1], email=data[2])
                # add passing records to this `passed` list
                users_passed.append(user)
            except ValidationError as e:
                q_data = ",".join(data)
                errors = e.errors()
                # add erroneous records to the `quarantine` list
                # along with the records of the error
                # `errors` would contain the error details
                # and can be further processed to be more concise
                users_quarantined.append((q_data, errors))
```

Printing some information about this flow

```python
print(f"Total rows processed: {clines}")
print(f"Total rows passed: {len(users_passed)}")
print(f"Total rows quarantined: {len(users_quarantined)}")

print()
print("----passed------\n", users_passed)
print()
print("----quarantined------\n", users_quarantined)
print()
```


Will result in

```bash
Total rows processed: 5
Total rows passed: 4     
Total rows quarantined: 1

----passed------
 [User(id=1001, name='ana', email='ana@example.com'), User(id=1002, name='isabel', email='isabel@example.com'), User(id=1003, name='kris', email='kris@example.com'), User(id=1004, name='bee', email='bee@example.com')]

----quarantined------
 [('100s,kim,jan@example.com', [{'type': 'int_parsing', 'loc': ('id',), 'msg': 'Input should be a valid integer, unable to parse string as an integer', 'input': '100s', 'url': 'https://errors.pydantic.dev/2.7/v/int_parsing'}])]
```

This example can be further extended for more complex data.