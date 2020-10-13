#!python
# coding=utf-8

import pytest
import responses

from erddap_metrics.lib.erddap_metrics import ErddapMetrics


@pytest.fixture
def mocked_responses():
    # Use to mock calls to requests library
    # https://github.com/getsentry/responses
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        yield rsps


@pytest.fixture
def erddap_server_metrics():
    erddap_metrics = ErddapMetrics(settings_file='tests/test_settings.yml', skip_scheduling=True)
    erddap_metrics.reset_metrics()
    return erddap_metrics
