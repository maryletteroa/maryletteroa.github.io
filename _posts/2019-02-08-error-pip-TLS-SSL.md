---
layout: post
title: Pip is configured with locations that require TLS/SSL, however the ssl module in Python is not available
categories: [blog]
tags: [python]
---

```
pip3 install pep8

pip is configured with locations that require TLS/SSL, however the ssl module in Python is not available.
```
[^1]

Getting this error proved to be time consuming not just because a Python project often starts with `pip` (i.e. downloading libraries) but also because troubleshooting could take up so much time. In my case, I think this was brought about by fiddling with the installation of `Bash on Ubuntu on Windows` in my local machine. 

But I guess the moral of the story is -- sometimes in life you can just spend much of the day troubleshooting (or installing!), and that's okay.

The solution is to install [OpenSSL](https://www.openssl.org/source/) - if you don't have one installed. Find out using

```bash
openssl version
```

<!--more-->

(If it is installed and working, you'll need another workaround.)

After doing much "Google-fu", here is the method that worked for me [^2]. 

```bash
mkdir /tmp
cd /tmp
wget https://www.openssl.org/source/openssl-1.1.1a.tar.gz
tar -xvf openssl-1.1.1a.tar.gz
cd openssl-1.1.1a
./config --prefix=/usr/local/openssl --openssldir=/usr/local/openssl
make
make install
```

Then re-install Python from source [^3]


```bash
cd /tmp
wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz #get the version that works for you
tar xzf Python-3.7.2.tgz
cd Python-3.7.2
./configure --enable-optimizations --with-openssl=/usr/local/openssl
make altinstall #if you have other versions of python installed use altinstall instead of install
```

Alternatively, if you have the source compiled already, clean it out first
```bash
make clean
make distclean
```
Then, proceed with compilation and installation.

Test again

```bash
pip3 install pep8
```
### Footnotes:

[^1]: Actually, it's [pycodestyle](https://pypi.org/project/pycodestyle/) now
[^2]: [https://stackoverflow.com/questions/3016956/how-do-i-install-the-openssl-libraries-on-ubuntu](https://stackoverflow.com/questions/3016956/how-do-i-install-the-openssl-libraries-on-ubuntu)
[^3]: [https://tecadmin.net/install-python-3-7-on-ubuntu-linuxmint/](https://tecadmin.net/install-python-3-7-on-ubuntu-linuxmint/)
