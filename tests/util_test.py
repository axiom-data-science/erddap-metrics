#!python
# coding=utf-8
from datetime import datetime

import pytest
from dateutil import tz

from erddap_metrics.lib.util import requests_get, dt_from_utc_str


def test_dt_from_utc_str():
    assert dt_from_utc_str('2019-12-27T23:00:24Z') == datetime(2019, 12, 27, 23, 00, 24, tzinfo=tz.tzutc())
    assert dt_from_utc_str(None) is None


@pytest.mark.skip(reason="integration tests, run manually only")
class TestUtilsRequests():

    def test_requests_get__text(self):
        url = 'http://erddap.cencoos.org/erddap/status.html'
        result = requests_get(url)
        print(result)

    def test_requests_get__csv(self):
        url = 'http://erddap.cencoos.org/erddap/tabledap/allDatasets.csv?datasetID%2CmaxTime'
        result = requests_get(url, result_type='csv')
        print(result)
