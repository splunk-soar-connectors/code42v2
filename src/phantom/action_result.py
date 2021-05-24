class ActionResult:
    def __init__(self, param):
	    self._dict = {"parameters": param, "data": []}

    def add_data(self, data):
	    self._dict["data"].append(data)

    def set_status(self, status, status_message=None, exception=None):
        self._dict["status"] = status
        if exception:
            message = f"Error string: '{str(exception)}"
            if status_message:
                message = 

        if status_message is None:
            return

        self.data.setdefault("exceptions", []).append(
            {"exc_info": exc_info, "exception": exception}
        )

    def get_data(self):
        return self.data["data"]

    def set_summary(self, summary):
        self._dict["summary"] = summary

    def update_summary(self, message):
        summary = self._dict.get("summary")
        if not summary:
            self.set_summary(message)
        else:
            summary.update(message)
