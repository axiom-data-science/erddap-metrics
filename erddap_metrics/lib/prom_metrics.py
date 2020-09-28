#!python
# coding=utf-8

from prometheus_client import Gauge

from erddap_metrics.lib.erddap_metrics import ErddapMetrics
from erddap_metrics.lib.singleton import Singleton


class PromMetrics(metaclass=Singleton):
    def __init__(self, erddap_metrics=None):
        self.erddap_metrics = erddap_metrics or ErddapMetrics()
        self.gauges = {}

    def update_gauges(self):
        """Convert metrics from ErddapMetrics into Prometheus metrics."""
        metrics = self.erddap_metrics.get_metrics()
        for metric in metrics:
            if metric.metric_value is None:
                # should never be returned by ErddapMetrics... but just to be safe
                continue
            if metric.name not in self.gauges.keys():
                # note: declaring a Gauge here adds it to the list of metrics tracked by Prometheus
                self.gauges[metric.name] = Gauge(metric.name, metric.help, metric.label_names)
            self.gauges[metric.name].labels(*metric.label_values).set(metric.metric_value)
