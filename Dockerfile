FROM ubuntu:14.04
MAINTAINER Binh Nguyen

RUN apt-get update -y && apt-get install -y
	python-dev \
	python-pip \
	git \
	wget

WORKDIR /home/ubuntu
ADD . .
RUN wget https://bootstrap.pypa.io/ez_setup.py -O - | python
RUN python setup.py install


CMD python consumer.py
