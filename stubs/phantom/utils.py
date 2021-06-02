import re


def is_md5(input_str):
    rex = "^[0-9a-fA-F]{32}$"
    m = re.match(rex, input_str)
    return m is not None


def is_sha256(input_str):
    regex = "^[0-9a-fA-F]{64}$"
    m = re.match(regex, input_str)
    return m is not None
