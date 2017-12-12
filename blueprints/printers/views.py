from flask import Blueprint

printer_blueprint = Blueprint("printer", __name__)


@printer_blueprint.route('/hello_world')
def print_hello_world():
    return 'Hello, World!'


@printer_blueprint.route('/hello_world2')
def print_hello_world2():
    return 'Hello, World2!'


