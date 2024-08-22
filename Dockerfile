# THE GENERAL CONTAINER FOR CONNECTING ALL THE ENVIRONMENTS 😈
FROM ubuntu:22.04

#SYSTEM
ARG DEBIAN_FRONTEND=noninteractive
RUN usermod -s /bin/bash root
RUN apt-get update 

#RUST
RUN apt-get install curl nano build-essential cargo libstd-rust-dev -y

#NODE 
RUN apt-get install -y nodejs npm
RUN npm install -g pm2 

#PYTHON
RUN apt-get install python3.10 python3-pip -y
ENV LIBNAME commune
RUN git clone https://github.com/commune-ai/commune.git /commune 
RUN pip install -e /commune
RUN pip install communex
RUN pip install bittensor


ENV PWD /app
WORKDIR /app

# IMPORT EVERYTHING ELSE
ENTRYPOINT [ "tail", "-f", "/dev/null"]