#!python
# coding=utf-8
from pathlib import Path

from tests import test_helper


def test_initial_metrics(erddap_server_metrics):
    metrics = erddap_server_metrics.get_metrics()
    assert 0 == len(metrics)


def test_update_metrics__server_loaded(erddap_server_metrics, mocked_responses):
    status_page_html = _read_test_file('data/erddap_status_page.html')
    test_helper._stub_request(mocked_responses, status_page_html)

    erddap_server_metrics.update_metrics()

    metrics = erddap_server_metrics.get_metrics()

    # verify only one region
    for metric in metrics:
        assert ['testing'] == metric.label_values

    # check values
    _assert_value(metrics, 'erddap_server_status', 1)

    _assert_value(metrics, 'erddap_server_num_datasets', 2046)
    _assert_value(metrics, 'erddap_server_num_grid_datasets', 2)
    _assert_value(metrics, 'erddap_server_num_table_datasets', 2044)

    _assert_value(metrics, 'erddap_server_mins_since_last_refresh', 4)
    _assert_value(metrics, 'erddap_server_last_refresh_seconds', 5)
    _assert_value(metrics, 'erddap_server_num_failed_load_datasets', 6)

    _assert_value(metrics, 'erddap_server_num_recent_success_responses', 8389)
    _assert_value(metrics, 'erddap_server_num_recent_failed_responses', 1)


def test_update_metrics__server_updating(erddap_server_metrics, mocked_responses):
    status_page_html = _read_test_file('data/erddap_status_page_updating.html')
    test_helper._stub_request(mocked_responses, status_page_html)

    erddap_server_metrics.update_metrics()

    metrics = erddap_server_metrics.get_metrics()

    _assert_value(metrics, 'erddap_server_status', 1)
    _assert_value(metrics, 'erddap_server_num_datasets', 546)

    # shouldn't set these gauges, since erddap is still updating
    _assert_value(metrics, 'erddap_server_mins_since_last_refresh', None)
    _assert_value(metrics, 'erddap_server_last_refresh_seconds', None)


def test_updates_metrics__server_updating_initial_load(erddap_server_metrics, mocked_responses):
    status_page_html = _read_test_file('data/erddap_status_page_init.html')
    test_helper._stub_request(mocked_responses, status_page_html)

    erddap_server_metrics.update_metrics()

    metrics = erddap_server_metrics.get_metrics()

    _assert_value(metrics, 'erddap_server_status', 1)

    # shouldn't set these gauges, since erddap is initializing
    _assert_value(metrics, 'erddap_server_num_datasets', 0)
    _assert_value(metrics, 'erddap_server_num_failed_load_datasets', None)
    _assert_value(metrics, 'erddap_server_mins_since_last_refresh', None)


def test_update_metrics__handles_error(erddap_server_metrics, mocked_responses):
    status_page_html = _read_test_file('data/erddap_status_page_502_error.html')
    test_helper._stub_request(mocked_responses, status_page_html)

    erddap_server_metrics.update_metrics()

    metrics = erddap_server_metrics.get_metrics()

    _assert_value(metrics, 'erddap_server_status', 0)

    # shouldn't set these gauges, since erddap is down
    _assert_value(metrics, 'erddap_server_num_datasets', None)
    _assert_value(metrics, 'erddap_server_num_failed_load_datasets', None)
    _assert_value(metrics, 'erddap_server_mins_since_last_refresh', None)


def _assert_value(metrics, name, expected_value):
    if expected_value is None:
        assert 0 == len([m for m in metrics if m.name == name])
    else:
        metric = next(m for m in metrics if m.name == name)
        assert expected_value == metric.metric_value


def _read_test_file(path):
    with open(Path('tests', path), 'r') as f:
        return f.read()
