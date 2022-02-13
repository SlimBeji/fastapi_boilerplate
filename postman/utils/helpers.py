import base64
import hashlib
import json
import os
import re
from textwrap import wrap
from unicodedata import normalize

from unidecode import unidecode


def beautify_number(f, decimals=0, symbol="", to_percentage=False):
    try:
        f = float(f)
    except Exception:
        return f
    if to_percentage:
        f = f * 100
    negative = True if f < 0 else False
    sign = "-" if negative else ""
    f_str = str(abs(int(float(f))))
    f_str = ",".join(wrap(f_str[::-1], 3))[::-1]
    if decimals:
        f_decimals = "{0:.{precision}}".format(f - int(f), precision=decimals)
        if not negative:
            decimals_str = f_decimals[2 : 2 + decimals]
        else:
            decimals_str = f_decimals[3 : 3 + decimals]

        decimals_str = (decimals_str + "0" * decimals)[:decimals]
        f_str = "%s.%s" % (f_str, decimals_str)

    if symbol.strip() in ["$"]:
        f_str = "%s%s%s" % (sign, symbol, f_str)
    else:
        f_str = "%s%s%s" % (sign, f_str, symbol)

    return f_str


def from_text_to_name(text, hyphenate=False):
    text = normalize("NFKC", text)
    name = unidecode(text)
    space_replacement = ""
    if hyphenate:
        space_replacement = "-"
    name = name.lower().replace(" ", space_replacement)
    name = "".join(
        letter for letter in name if letter.isalnum() or letter == "-"
    )
    return name


def timedelta_to_string(td):
    result = re.sub(r"^0:", "", str(td))
    if len(result.split(":")[0]) == 1:
        result = "0" + result
    return result


def parse_db_url(database_url):
    client_str = database_url.split("://")[0]
    database_url = database_url.lstrip(f"{client_str}://")

    user = database_url.split("@")[0].split(":")[0]
    password = database_url.split("@")[0].split(":")[1]
    database_url = database_url.lstrip(f"{user}:{password}")[1:]
    host = database_url.split(":")[0]
    port = database_url.split("/")[0].split(":")[1]
    database_name = database_url.split("/")[1]

    return {
        "client": client_str,
        "user": user,
        "password": password,
        "host": host,
        "port": port,
        "db": database_name,
    }


def flatten_json(nested_json, exclude=None):
    """Flatten json object with nested keys into a single level.
    use "exclude" argument to exclude  keys"""
    out = {}

    def flatten(x, name="", exclude=exclude):
        if exclude is None:
            exclude = [""]
        if type(x) is dict:
            for a in x:
                if a not in exclude:
                    flatten(x[a], name + a + "_")
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + "_")
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out


def encode_values(**kwargs):
    value_json = json.dumps(kwargs)
    value_bytes = value_json.encode()
    encoded = base64.b64encode(value_bytes)
    result = encoded.decode()
    return result


def decode_values(code):
    if not code:
        return {}

    try:
        result_bytes = base64.b64decode(code.encode())
        result_string = result_bytes.decode()
        result = json.loads(result_string)
    except Exception:
        return {}

    return result


def hash_file(file_path):
    BUF_SIZE = 65536
    hasher = hashlib.sha1()
    with open(file_path, "rb") as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()


def get_file_properties(file_path, with_content=True, encoding="utf-8"):
    file_stats = os.stat(file_path)
    result = {
        "sha": hash_file(file_path),
        "size": file_stats.st_size,
    }
    if with_content:
        with open(file_path, "r", encoding=encoding) as f:
            result["content"] = f.read()
    return result
