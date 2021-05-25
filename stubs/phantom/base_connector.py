class BaseConnector:
    def __init__(self):
        self._action_results = []

    def add_action_result(self, action_result):
        self._action_results.append(action_result)
        return action_result

    def get_action_results(self):
        return self._action_results

    def save_progress(self, status):
        pass

    def get_action_identifier(self):
        pass

    def debug_print(self, name, value):
        pass

    def load_state(self):
        pass

    def get_config(self):
        pass

    def save_state(self, state):
        pass

    @classmethod
    def _get_phantom_base_url(cls):
        pass

    def _handle_action(self, param, param2):
        pass

    def _set_csrf_info(self, token, referer):
        pass
