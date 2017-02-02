flow - Auth
===========

## -2. Ports Used:

8881

## -1. Preface:

These commands have only been tested on 16.04 & 16.10 but that doesn't mean that they won't work on other distros.

## 0. Software Requirements:

### To install Python 3.6 and virtualenv

If on Ubuntu 16.04:

```
sudo add-apt-repository ppa:jonathonf/python-3.6
```

Then on Ubuntu 16.[04/10]:

```
sudo apt-get update
sudo apt install python3.6 virtualenv;
```

## 1. Python Requirements

If on Ubuntu 16.[04/10]:

```
cd flow/auth
virtualenv -p python3.6 .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Run

```
python server.py
```
