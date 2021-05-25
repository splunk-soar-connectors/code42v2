ACTION_MAP = {}

def action_key(key):
    def wrapper(f):
        ACTION_MAP[key] = f
        return f

    return wrapper

@action_key("foo")
def test_func():
    pass

if __name__ == "__main__":
    print("blep")
    print(ACTION_MAP)
