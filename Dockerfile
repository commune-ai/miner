FROM ubuntu:22.04
FROM python:3.12.3-bullseye
ENV PWD /app
WORKDIR /app
ARG DEBIAN_FRONTEND=noninteractive
RUN usermod -s /bin/bash root
# RUST
COPY ./scripts /app/scripts
RUN ./scripts/install_node.sh
RUN ./scripts/install_python.sh
RUN ./scripts/install_commune.sh
ENTRYPOINT [ "tail", "-f", "/dev/null"]