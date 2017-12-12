from enum import Enum
from flask.json import jsonify


class HttpStatusCode(Enum):
    OK = 200
    RESOURCE_CREATED = 201
    CONFLICT = 409
    INTERNAL_SERVER_ERROR = 500


class JsonError(ValueError):

    def __init__(self, msg):
        super(JsonError, self).__init__(msg)


class JsonResponse:

    _MSG_JSON_KEY = "msg"

    def __init__(self, status_code, msg):
        self._msg = msg
        self._status_code = status_code

    @property
    def msg(self):
        return self._msg

    @property
    def status_code(self):
        return self._status_code

    @property
    def to_response(self):
        return jsonify({self._MSG_JSON_KEY: self._msg}), self._status_code.value


class JsonErrorResponse:

    _ERROR_MSG_JSON_KEY = "error_msg"

    def __init__(self, status_code, error):
        self._error = error
        self._status_code = status_code

    @property
    def error_msg(self):
        return self._error

    @property
    def status_code(self):
        return self._status_code

    @property
    def to_response(self):
        return jsonify({self._ERROR_MSG_JSON_KEY: self._error.message}), self._status_code.value

