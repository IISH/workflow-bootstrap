from flask import Blueprint

health_blueprint = Blueprint('health', __name__)


@health_blueprint.route('/ping')
def ping():
    return pingm('pong')


@health_blueprint.route('/ping/<message>')
def pingm(message):
    return {'status': 200, 'message': message}
