"""
 # @ Author: Marylette Roa
 # @ Create Time: 2024-06-29 15:44:20
 # @ Modified by: Marylette Roa
 # @ Modified time: 2024-06-29 16:35:48
 """

from pydantic import BaseModel, EmailStr, model_validator
from pydantic_core import ValidationError


class User(BaseModel):
    id: int
    name: str
    email: EmailStr

    @model_validator(mode="before")
    @classmethod
    def correct_email(cls, data: dict):
        # remove space in email address
        data["email"] = data["email"].replace(" ", "")
        return data


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
                users_passed.append(user)
            except ValidationError as e:
                q_data = ",".join(data)
                errors = e.errors()
                users_quarantined.append((q_data, errors))


print(f"Total rows processed: {clines}")
print(f"Total rows passed: {len(users_passed)}")
print(f"Total rows quarantined: {len(users_quarantined)}")

print()
print("----passed------\n", users_passed)
print()
print("----quarantined------\n", users_quarantined)
print()
