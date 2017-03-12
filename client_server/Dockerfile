FROM ubuntu:16.04

# Update OS
#RUN sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list

RUN apt-get update
RUN apt-get install -y software-properties-common python-software-properties
RUN add-apt-repository -y ppa:jonathonf/python-3.6
RUN apt-get update
RUN apt-get install -y python3.6 python3.6-dev python3-pip


COPY . /app
ENV HOME /app
WORKDIR /app

RUN python3.6 -m pip install -r requirements.txt
EXPOSE 8882

#ENTRYPOINT ["python3.6", "server.py"]

CMD python3.6 server.py


# Install uwsgi Python web server
#RUN pip install uwsgi


#RUN ls -a

# Create app directory
#COPY . /webapp

# Set the default directory for our environment
#ENV HOME /webapp
#WORKDIR /webapp


# Install app requirements
#RUN pip install -r requirements.txt

# Expose port 8000 for uwsgi
#EXPOSE 8000
