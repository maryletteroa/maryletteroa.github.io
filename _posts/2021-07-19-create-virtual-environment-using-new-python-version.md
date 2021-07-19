---
layout: post
title: Create a virtual environment using a new version of Python
categories:
- blog
---

Install the version e.g. Python version 3.9:

```bash
sudo apt update
# sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.9
```

Install the development libraries
```bash
sudo  apt-get install python3.9-dev python3.9-venv
```

Specify Python version when creating a virtual environment
```bash
virtualenv --python=/usr/bin/python3.9 env

# or
# python3.9 -m venv env
```