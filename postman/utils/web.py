import json
import os
import urllib
from urllib.parse import unquote, urlparse

import requests

from .helpers import from_text_to_name


def check_url(url):
    try:
        res = urllib.request.urlopen(url)
        if res.code == 200:
            return True
        return False
    except Exception:
        return False


def extract_url_param(url, param):
    parsed = urlparse(url)
    query = parsed.query
    query_dict = urllib.parse.parse_qs(query)

    result = None
    if param in query_dict:
        result = query_dict[param]
        if len(result) == 1:
            result = result[0]

    return result


def replace_url_param(url, param, value):
    parsed = urlparse(url)
    query = parsed.query
    query_dict = urllib.parse.parse_qs(query)
    query_dict[param] = value
    new_query = urllib.parse.urlencode(query_dict, doseq=True)
    parsed = parsed._replace(query=new_query)
    return urllib.parse.urlunparse(parsed)


def delete_url_param(url, param):
    parsed = urlparse(url)
    query = parsed.query
    query_dict = urllib.parse.parse_qs(query)
    if param in query_dict:
        query_dict.pop(param)
    new_query = urllib.parse.urlencode(query_dict, doseq=True)
    parsed = parsed._replace(query=new_query)
    return urllib.parse.urlunparse(parsed)


def get_file_name_from_url(url):
    a = urlparse(unquote(url))
    file_name = os.path.basename(a.path)

    return file_name


def get_json_from_url(url):
    response = requests.get(url)
    result = json.loads(response.content)
    return result


def from_text_to_url(
    text, with_protocol=False, protocol="https", domain_name="example.com"
):
    project_name = from_text_to_name(text)
    project_url = f"{project_name}.{domain_name}"
    if with_protocol:
        project_url = f"{protocol}://{project_url}"

    return project_url


def get_image_file(img_url, user_agent=None):
    image_file_name = get_file_name_from_url(img_url)
    if user_agent:
        req = urllib.request.Request(
            img_url,
            headers={"User-Agent": user_agent},
        )
        with urllib.request.urlopen(req) as response:
            with open(image_file_name, "wb") as f:
                f.write(response.read())
    else:
        urllib.request.urlretrieve(img_url, image_file_name)

    return image_file_name
