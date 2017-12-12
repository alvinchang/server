

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


class JsonErrorResponse:

    _ERROR_MSG_JSON_KEY = "error_msg"

    def __init__(self, status_code, error_msg):
        self._error_msg = error_msg
        self._status_code = status_code

    @property
    def error_msg(self):
        return self._error_msg

    @property
    def status_code(self):
        return self._status_code

