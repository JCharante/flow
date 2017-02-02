flow - queue
===========

## 1. Ports Used:

* 8883 (restful api)
* 8884 (websocket)

## 2. Preface:

These commands have only been tested on 16.04 & 16.10 but that doesn't mean that they won't work on other distros.

## 3. Software Requirements:

### To install Python 3.6 and virtualenv

If on Ubuntu 16.04:

```
sudo add-apt-repository ppa:jonathonf/python-3.6
```

Then on Ubuntu 16.[04/10]:

```
sudo apt-get update
sudo apt install python3.6 virtualenv mysql-server pymysql
```

When prompted for a root username & password, I usu `root` & `root` `¯\_(ツ)_/¯`

## 4. Database Setup

Now that you have mysql, you should create the user that the servers will use.

In this example, we'll use `'queue'@'localhost'`, with the password `queue`

```
$ mysql -u root -p
Enter Password: root
mysql> CREATE USER 'queue'@'localhost' IDENTIFIED BY 'queue';
mysql> GRANT ALL PRIVILEGES ON *.* TO 'queue'@'localhost';
mysql> FLUSH PRIVILEGES;
mysql> create database queue;
mysql> quit;
```

## 5. Python Requirements

If on Ubuntu 16.[04/10]:

```
cd flow/queue
virtualenv -p python3.6 .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 6. Run

```
python server.py
```
