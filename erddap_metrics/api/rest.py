#!python
# coding=utf-8
import hug

from erddap_metrics.lib.erddap_metrics import ErddapMetrics, ErddapGauge


@hug.output_format.json_convert(ErddapGauge)
def erddap_gauge_stringable(gauge):
    return gauge.__dict__


@hug.get('/all', version=1)
def get_all_metrics(response):
    return ErddapMetrics().get_metrics()


@hug.get('/by_region', examples='region=testing', version=1)
def get_metrics_for_region(region: str, response):
    return ErddapMetrics().get_metrics_for_region(region)
