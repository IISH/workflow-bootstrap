from flask import Blueprint, request, abort, Response, send_file
import uuid
import os
import re

csr_blueprint = Blueprint('csr', __name__)

AUTOSIGN = os.environ.get('AUTOSIGN', '0').lower().strip() in ['true', 't', '1', 'yes', 'y']
CSR_DIR = os.environ.get('CSR_DIR', './csr')
AUTOSIGN_DIR = os.environ.get('AUTOSIGN_DIR', './sign')
CERTS_DIR = os.environ.get('CERTS_DIR', './certs')
SIGNED_DIR = os.environ.get('SIGNED_DIR', './signed')
UUID_PATTERN = "^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$"


@csr_blueprint.route('/ca', methods=['GET'])
def get_ca():
    filename = CERTS_DIR + '/ca.cert'
    return Response(readfile(filename), status=200, mimetype='text/plain')


@csr_blueprint.route('/client-cert', methods=['GET'])
def get_client_config():
    filename = CERTS_DIR + '/client-cert.conf'
    return Response(readfile(filename), status=200, mimetype='text/plain')


# Gebruik bij de post de header application/text
@csr_blueprint.route('/csr', methods=['POST'])
def csr_opslaan():
    data = request.data
    if data.__len__() == 0 or data.__len__() > 10240:
        abort(500)

    identifier = uuid.uuid4().__str__().lower()
    filename = CSR_DIR + '/' + identifier + '.csr'
    with open(filename, 'wb') as f:
        f.write(data)

    if AUTOSIGN:
        filename_autosign = AUTOSIGN_DIR + '/' + identifier + '.csr'
        os.rename(filename, filename_autosign)

    return Response(identifier, status=200, mimetype='text/plain')


@csr_blueprint.route('/csr/<identifier>', methods=['GET'])
def certificaat_pakken(identifier: str):
    if not re.match(UUID_PATTERN, identifier):
        return Response('Invalid identifier. Should be a UUID4 formatted string: ' + UUID_PATTERN, status=400,
                        mimetype='text/plain')

    filename = SIGNED_DIR + '/' + identifier + '.pem'
    if os.path.exists(filename):
        return Response(readfile(filename), status=200, mimetype='text/plain')
    else:
        return Response('Certificate not found. Try again in one minute.', status=404, mimetype='text/plain')


def readfile(filename):
    with open(filename, 'r') as f:
        return f.readlines()
