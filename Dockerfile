FROM ubuntu:jammy
LABEL Description="Temporal bootstrap client certificates" Version="v1.0.0"

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED 1
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV LC_LANG=en_US.UTF-8
ENV TZ=Europe/Amsterdam
ENV CERTS_DIR=./certs
ENV KEYS_DIR=./privat
ENV CSR_DIR=./csr
ENV AUTOSIGN_DIR=./autosign
ENV AUTOSIGN=1

WORKDIR /opt

RUN apt-get update && apt-get upgrade -y && apt-get install python3.10 python3-pip -y && pip install --upgrade pip && \
    mkdir csr certs autosign private signed


COPY *.py .
COPY requirements.txt .

RUN /usr/bin/pip install -r requirements.txt && rm requirements.txt

CMD ["/usr/local/bin/gunicorn", "--workers", "1", "--bind", "0.0.0.0:8000", "main:app"]