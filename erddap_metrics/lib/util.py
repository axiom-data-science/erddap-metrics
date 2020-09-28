#!python
# coding=utf-8

import logging

import requests


def requests_get(url):
    logging.debug(f'GET {url}')

    response = requests.get(url, allow_redirects=True)
    if response.status_code != 200:
        message = f"GET {url}: HTTP {response.status_code}: {response.text}"
        logging.error(message)
        raise requests.exceptions.HTTPError(message)
    return response.text
