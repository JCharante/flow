flow - Client Server
===========

## 1. Ports Used:

8882

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
sudo apt install python3.6 virtualenv;
```

## 4. Python Requirements

If on Ubuntu 16.[04/10]:

```
cd flow/client_server
virtualenv -p python3.6 .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 5. Run

```
python server.py
```

Run with Docker
===============

(Aimed at hosting locally)

##### 1. Install the dependencies

On Ubuntu 16.04:

```
sudo apt install docker.io
```

##### 2. Set the directory of this file as your active directory.

##### 3. Build the docker image


```
sudo docker build -t client_server-img .
```

##### 4. Run the docker image in a container

```
sudo docker run -d -p 8882:8882 --restart=always --name client_server client_server-img
```

##### 5. To find out the address

```
docker inspect --format '{{ .NetworkSettings.IPAddress }}' client_server
```

Then go to the address in the output with the port 8882 in your browser.

By default http://0.0.0.0:8882 should work.

##### To stop & delete the container

```
sudo docker stop client_server
sudo docker rm client_server
```

##### To update the container to new code

```
# Stopping & Deleting the container
sudo docker stop client_server
sudo docker rm client_server
# Rebuilding image
sudo docker rmi client_server-img
sudo docker build -t client_server-img .
# Launching the container
sudo docker run -d -p 8882:8882 --restart=always --name client_server client_server-img
# Getting the address
docker inspect --format '{{ .NetworkSettings.IPAddress }}' client_server
```