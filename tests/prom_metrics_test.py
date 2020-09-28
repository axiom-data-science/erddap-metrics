#!python
# coding=utf-8
from erddap_metrics.lib.prom_metrics import PromMetrics
from tests import test_helper
from tests.erddap_metrics_test import _read_test_file


def test_converts_erddap_metrics_to_prom_gauges(erddap_server_metrics, mocked_responses):
    prom_metrics = PromMetrics(erddap_server_metrics)

    assert 0 == len(prom_metrics.gauges)

    # successfully initialized server
    status_page_html = _read_test_file('data/erddap_status_page.html')
    test_helper._stub_request(mocked_responses, status_page_html)
    erddap_server_metrics.update_metrics()

    prom_metrics.update_gauges()
    prom_metrics.update_gauges()

    gauges = prom_metrics.gauges

    assert 9 == len(gauges)

    # prom doesn't expose attributes on their Gauge class...
    # so if we got here then there weren't any errors  ¯\_(ツ)_/¯
