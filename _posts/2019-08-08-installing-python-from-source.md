---
layout: post
title: "Installing Python from source (Ubuntu)"
date: 2019-08-08
tags: [python]
categories: [misc]
---

Get the link for the source code from the [Python Software Foundation](https://www.python.org/downloads/release).

Run the following in the terminal.

```sh
sudo apt update
sudo apt install build-essential \
        zlib1g-dev libncurses5-dev libgdbm-dev \
        libnss3-dev libssl-dev libreadline-dev \
        libffi-dev wget

cd /tmp
wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tgz
tar -xvf Python-3.7.4.tgz
cd Python-3.7.4
sudo ./configure --enable-optimizations --with-openssl=/usr/bin/openssl
sudo make altinstall -j `nproc`
```
<!--more-->

Sidenotes:
* Linking OpenSSL just in case `pip` can't find it
* `nproc` outputs the number of processors in the computer

For in-depth discussion check this source: [Linuxize](https://linuxize.com/post/how-to-install-python-3-7-on-ubuntu-18-04).