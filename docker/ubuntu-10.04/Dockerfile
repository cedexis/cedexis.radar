FROM ubuntu:10.04

MAINTAINER Jacob Wan <jacob@wildlemur.com>
RUN apt-get update && apt-get install -y git-core python-software-properties
RUN add-apt-repository ppa:fkrull/deadsnakes \
    && apt-get update \
    && apt-get install -y \
    python2.7 \
    python-setuptools-deadsnakes \
    && easy_install-2.7 pip \
    && pip2.7 install cedexis.radar
