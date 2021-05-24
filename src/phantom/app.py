APP_ERROR = False
APP_SUCCESS = True
APP_SUCCESS_STR = 'success'
APP_ERROR_STR = 'failed'

def get_succ_or_failure_text(status_code):
    if not status_code:
        return APP_ERROR_STR
    else:
        return APP_SUCCESS_STR