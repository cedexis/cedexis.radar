FROM ubuntu:10.04

MAINTAINER Jacob Wan <jacob@wildlemur.com>
RUN apt-get update && apt-get install -y git-core python-software-properties
RUN add-apt-repository ppa:fkrull/deadsnakes && apt-get update && apt-get install -y python2.7 python-setuptools-deadsnakes

RUN git clone https://github.com/cedexis/cedexis.radar.git && cd cedexis.radar && python2.7 setup.py install
