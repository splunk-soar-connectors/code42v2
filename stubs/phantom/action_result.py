from phantom.app import APP_ERROR

class ActionResult:
    def __init__(self, param):
        self._status_code = APP_ERROR
        self._status_message = ""
        self._data = []
        self._summary = {}
        if param is None:
            param = dict()
        if type(param) != dict:
            raise TypeError("param can only be a dictionary")
        self._param = param

    def add_data(self, item):
        self._data.append(item)

    def get_data(self):
        return self._data

    def get_param(self):
        return self._param

    def set_status(self, status_code, status_message="", exception=None):
        if type(status_code) != bool:
            raise TypeError("status_code is not of type bool")
        self._status_code = status_code
        self._status_message = status_message

        if exception:
            self._status_message = f"{self._status_message}. Error string: '{self._get_exception_str(exception)}'"

        return self._status_code

    def get_status(self):
        return self._status_code

    def get_message(self):
        return self._status_message

    def update_summary(self, summary):
        self._summary.update(summary)
        return self._summary

    def get_summary(self):
        return self._summary

    def _get_exception_str(self, exception):
        try:
            return getattr(exception, "message", exception)
        except:
            return ""
