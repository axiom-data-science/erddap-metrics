#!python
# coding=utf-8

import re
from datetime import datetime
from enum import Enum
from typing import List

import yaml
from apscheduler.schedulers.background import BackgroundScheduler

from erddap_metrics import logger
from erddap_metrics.lib import util
from erddap_metrics.lib.singleton import Singleton
from erddap_metrics.lib.util import str2bool


class GaugeBool(Enum):
    UP = 1
    DOWN = 0


class ErddapGauge():
    """Erddap metric that maps to a Prometheus Gauge."""

    def __init__(self, name, help_text, region, value, dataset_id=None):
        self.name = name
        self.help = help_text
        self.region = region
        self.metric_value = value
        self.label_names = ['region']
        self.label_values = [region]
        if dataset_id:
            self.label_names.append('dataset_id')
            self.label_values.append(dataset_id)

    def __str__(self):
        return f"{self.name}[{self.region}] = {self.metric_value}"


def status_metric(region, value: GaugeBool):
    return ErddapGauge('erddap_server_status', 'ERDDAP Server status. [1=UP, 0=DOWN]', region, value.value)


class ErddapMetrics(metaclass=Singleton):
    """Provides all the relevant metrics for a given set of ERDDAP servers."""

    def __init__(self, settings_file='settings.yml', skip_scheduling=False):
        with open(settings_file, 'r') as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)

        # the list of ERDDAP servers to track
        self.regions_list = cfg['erddap_regions']
        for r in self.regions_list:
            if 'disable_dataset_metrics' not in r:
                r['disable_dataset_metrics'] = False
            else:
                r['disable_dataset_metrics'] = str2bool(r['disable_dataset_metrics'])
        logger.info(f"REGIONS: {self.regions_list}")

        self.metrics = []

        if skip_scheduling:
            # only for testing
            return

        # Creates a BackgroundScheduler with a MemoryJobStore and ThreadPoolExecutor with max count of 10
        # https://apscheduler.readthedocs.io/en/latest/userguide.html#configuring-the-scheduler
        scheduler = BackgroundScheduler()
        refresh_interval = int(cfg['refresh_interval_mins'])
        job = scheduler.add_job(self.update_metrics, 'interval', minutes=refresh_interval)
        scheduler.start()
        # run the job immediately to start out
        job.modify(next_run_time=datetime.now())

    def update_metrics(self):
        """Update metrics values."""
        logger.info('Updating metrics')
        metrics = []
        for region in self.regions_list:
            try:
                metrics.extend(self._metrics_for_region(region))
                if not region['disable_dataset_metrics']:
                    metrics.extend(self._dataset_metrics_for_region(region))
            except Exception:
                logger.error(f"Could not load metrics for '{region['name']}'!")
                metrics.append(status_metric(region['name'], GaugeBool.DOWN))
        self.metrics = metrics

    def get_metrics(self) -> List[ErddapGauge]:
        """Get latest metrics"""
        return self.metrics

    def get_metrics_for_region(self, region) -> List[ErddapGauge]:
        """Get latest metrics for a specific region."""
        return [m for m in self.metrics if m.region == region]

    def reset_metrics(self):
        """For testing only."""
        self.metrics = []

    # Internal

    def _metrics_for_region(self, region) -> List[ErddapGauge]:
        metrics = []

        region_name = region['name']
        logger.debug(f"Updating {region_name}")

        url = f"{region['base_url']}/status.html"
        status_page_text = util.requests_get(url)

        metrics.append(status_metric(region_name, GaugeBool.UP))

        def _first_result(pattern):
            return int(re.findall(pattern, status_page_text)[0])

        def _m(name, help_text, value):
            metrics.append(ErddapGauge(name, help_text, region_name, value))

        num_total_datasets = _first_result(r"nTotalDatasets\s+= (\d+)")
        _m('erddap_server_num_datasets', 'Total number of datasets on this server (nTotalDatasets)',
           num_total_datasets)
        _m('erddap_server_num_table_datasets', 'Total number of table datasets on this server (nTableDatasets)',
           _first_result(r"nTableDatasets\s+= (\d+)"))
        _m('erddap_server_num_grid_datasets', 'Total number of grid datasets on this server (nGridDatasets)',
           _first_result(r"nGridDatasets\s+= (\d+)"))

        if len(re.findall("ago and is still running.", status_page_text)) > 0:
            # skip last refresh metrics, since server is currently updating
            pass
        else:
            _m('erddap_server_mins_since_last_refresh', 'Minutes since Last major LoadDatasets',
               _first_result(r"Last major LoadDatasets started (\d+)m"))
            _m('erddap_server_last_refresh_seconds', 'How long (in seconds) it took for the last major LoadDatasets',
               _first_result(r"and finished after (\d+) seconds."))

        if num_total_datasets > 0:
            _m('erddap_server_num_failed_load_datasets',
               'Total number of table datasets that failed to load (n Datasets Failed To Load)',
               _first_result(r"n Datasets Failed To Load \(in the last major LoadDatasets\) = (\d+)"))

            _m('erddap_server_num_recent_success_responses', 'Number of successful responses since last Daily Report',
               _first_result(r"Response Succeeded Time \(since last Daily Report\)\s+n =\s+(\d+)"))
            _m('erddap_server_num_recent_failed_responses', 'Number of failed responses since last Daily Report',
               _first_result(r"Response Failed\s+Time \(since last Daily Report\)\s+n =\s+(\d+)"))

        return metrics

    def _dataset_metrics_for_region(self, region) -> List[ErddapGauge]:
        metrics = []

        region_name = region['name']
        logger.debug(f"Updating dataset metrics for {region_name}")

        url = f"{region['base_url']}/tabledap/allDatasets.csv?datasetID%2CmaxTime"
        all_datasets_csv = util.requests_get(url, result_type='csv')

        # convert the maxTime to seconds since last data point
        now = util.now()
        for d in all_datasets_csv:
            dataset_id = d['datasetID']
            try:
                last_data_point_time = util.dt_from_utc_str(d['maxTime'])
            except ValueError:
                logger.debug(f"Failed to parse {d}")
                continue
            seconds_since_last_data_point = (now - last_data_point_time).total_seconds()
            metrics.append(ErddapGauge('erddap_dataset_time_since_latest_data',
                                       'Number of seconds since the latest available data point for this dataset',
                                       region_name,
                                       seconds_since_last_data_point,
                                       dataset_id=dataset_id))

        return metrics
