from flask import Blueprint, request, abort, Response, send_file
import uuid
import os
import re

csr_blueprint = Blueprint('csr', __name__)

CERTS_DIR = os.environ.get('CERTS_DIR', './certs')
UUID_PATTERN = "^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$"


@csr_blueprint.route('/ca', methods=['GET'])
def get_ca():
    filename = CERTS_DIR + '/ca.cert'
    return send_file(filename, 'application/text')

@csr_blueprint.route('/csr', methods=['POST'])
def csr_opslaan():
    data = request.data
    if data.__len__() == 0 or data.__len__() > 10240:
        abort(500)

    identifier = uuid.uuid4().__str__().lower()
    filename = CERTS_DIR + '/' + identifier + '.csr'
    with open(filename, 'wb') as f:
        f.write(data)

    return Response(identifier, status=200, mimetype='application/text')


@csr_blueprint.route('/csr/<identifier>', methods=['GET'])
def certificaat_pakken(identifier: str):
    if not re.match(UUID_PATTERN, identifier):
        return Response('Invalid identifier. Should be a UUID4 formatted string: ' + UUID_PATTERN, status=400,
                        mimetype='application/text')

    filename = CERTS_DIR + '/' + identifier + '.pem'
    if not os.path.exists(filename):
        return Response('Certificate not found. Try again in one minute.', status=404, mimetype='application/text')

    return send_file(filename, 'application/text')