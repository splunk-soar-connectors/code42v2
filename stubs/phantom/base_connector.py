class BaseConnector:
    def __init__(self):
        self._action_results = []
        self._containers = []
        self._artifacts = []
        self._config = {}
        self._is_poll_now = False
        self._state = {}

    def is_poll_now(self):
        return self._is_poll_now

    def add_action_result(self, action_result):
        self._action_results.append(action_result)
        return action_result

    def get_action_results(self):
        return self._action_results

    def get_container_id(self):
        pass

    def save_progress(self, status):
        pass

    def get_action_identifier(self):
        pass

    def debug_print(self, name, value):
        pass

    def load_state(self):
        pass

    def get_config(self):
        return self._config

    def save_state(self, state):
        if not state:
            return
        if not self._state:
            self._state = {**state}
        else:
            self._state = {**state, **self._state}

    def save_container(self, container):
        self._containers.append(container)
        return True, None, "CONTAINER_ID"

    def save_artifacts(self, artifacts_list):
        self._artifacts.extend(artifacts_list)

    @classmethod
    def _get_phantom_base_url(cls):
        pass

    def _handle_action(self, param, param2):
        pass

    def _set_csrf_info(self, token, referer):
        pass
