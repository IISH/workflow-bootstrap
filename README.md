## installatie

    $ pip install --upgrade pip
    $ virtualenv p3venv
    $ ./p3venv/bin/python -m pip install --upgrade pip
    $ ./p3venv/bin/pip3 install --require-virtualenv --requirement requirements.txt

# Start in development (automatische herstart na code wijzigingen)

    $ ./p3venv/bin/python ./p3venv/bin/flask --app main.py --debug run

# Start in productie

    $ ./p3venv/bin/gunicorn --workers 1 --bind 0.0.0.0:8000 main:app

## De basis eenmalig: eigen CA met sleutel

Stel dat:

    CERTS_DIR=./certs
    CSR_DIR=./certs
    KEYS_DIR=./private

## De ca certificaat met met sleutel

    openssl genrsa -out "${KEYS_DIR}/ca.key" 4096
    openssl req -new -x509 -key "${KEYS_DIR}/ca.key" -sha256 -subj "/C=NL/ST=NH/O=KNAW HUC DI" -days 365 -out "${CERTS_DIR}/ca.cert"

## Voor clusters een certificaat en sleutel

    openssl genrsa -out "${KEYS_DIR}/cluster.key" 4096
    openssl req -new -key "${KEYS_DIR}/cluster.key" -out "${CSR_DIR}/cluster.csr" -config "${CERTS_DIR}/cluster-cert.conf"
    openssl x509 -req -in "${CSR_DIR}/cluster.csr" -CA "${CERTS_DIR}/ca.cert" -CAkey $CERTS_DIR/ca.key -CAcreateserial -out "${CERTS_DIR}/cluster.pem" -days 365 -sha256 -extfile "${CERTS_DIR}/cluster-cert.conf" -extensions req_ext

## Voor iedere worker / client een certificaat

    openssl req -newkey rsa:4096 -nodes -keyout "client.key" -out client.csr -config client-cert.conf
    openssl x509 -req -in client.csr -CA "${CERTS_DIR}/ca.cert" -CAkey "${KEYS_DIR}/ca.key" -CAcreateserial -out "${CERTS_DIR}/client.pem" -days 365 -sha256 -extfile client-cert.conf -extensions req_ext

## Een client request via de API

    export SERVER=http://localhost:5000
    export SERVER=https://dev-temporal-bootstrap.diginfra.net
    curl "${SERVER}/client-cert" -o 'client-cert.conf'
    openssl req -newkey rsa:4096 -nodes -keyout "client.key" -out client.csr -config client-cert.conf
    identifier=$(curl -H 'Content-Type: plain/text' --data-binary @client.csr "${SERVER}/csr")
    curl "${SERVER}/csr/${identifier}" -o 'client.cert'