#!python
# coding=utf-8

import hug
from prometheus_client import exposition

from erddap_metrics.lib.prom_metrics import PromMetrics

prom_metrics = PromMetrics()


@hug.get('/', version=1, output=hug.output_format.text)
def get_metrics(response):
    prom_metrics.update_gauges()
    content = exposition.generate_latest()
    return content.decode("utf-8")
