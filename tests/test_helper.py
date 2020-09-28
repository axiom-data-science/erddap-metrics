#!python
# coding=utf-8

import re

import responses


def _stub_request(mocked_responses, result, url_pattern=r'.*', request_type=responses.GET):
    """
    :param mocked_responses:  pass through the fixture here
    :param result:  string or dict to return
    :param url_pattern:  regular expression for url to match
    :param request_type: responses.GET, responses.POST, responses.HEAD, etc
    """
    mocked_responses.add(request_type, re.compile(url_pattern), body=result)
