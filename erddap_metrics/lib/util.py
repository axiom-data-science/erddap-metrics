#!python
# coding=utf-8
import codecs
import csv
from datetime import datetime

import requests
from dateutil import tz

from erddap_metrics import logger


def requests_get(url, result_type='text'):
    """
    :param url: url to GET
    :param result_type: text (default), json, or csv
    """
    logger.debug(f'GET {url}')

    try:
        response = requests.get(url, allow_redirects=True, timeout=30)
    except requests.exceptions.Timeout:
        message = f"GET {url}: Timed out"
        logger.error(message)
        raise requests.exceptions.HTTPError(message)
    if response.status_code != 200:
        message = f"GET {url}: HTTP {response.status_code}: {response.text}"
        logger.error(message)
        raise requests.exceptions.HTTPError(message)
    if result_type == 'json':
        return response.json()
    if result_type == 'csv':
        reader = csv.DictReader(codecs.iterdecode(response.iter_lines(), 'utf-8'))
        # returns list of dicts
        return list(reader)
    return response.text


def dt_from_utc_str(dtstr, pattern="%Y-%m-%dT%H:%M:%SZ", tzinfo=tz.tzutc()):
    return None if dtstr is None else datetime.strptime(dtstr, pattern).replace(tzinfo=tzinfo)


def now():
    return datetime.now().astimezone(tz.tzutc())


def str2bool(v):
    return v and str(v).lower() in ("yes", "true", "1")
