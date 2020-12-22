# erddap-metrics

[![Build Status](https://travis-ci.com/axiom-data-science/erddap-metrics.svg?branch=master)](https://travis-ci.com/axiom-data-science/erddap-metrics)

Provides ERDDAP metrics and status, via a REST API and Prometheus metrics endpoint.

## Quickstart

```
# get settings.yml template
wget "https://raw.githubusercontent.com/axiom-data-science/erddap-metrics/master/settings.yml.example" -O settings.yml
# edit as needed

# pull and run via docker
docker pull axiom/erddap-metrics:latest
docker run --rm --name erddap-metrics \
   -p 9102:9102  \
   -v $(pwd)/settings.yml:/app/settings.yml \
 erddap-metrics gunicorn --bind '0.0.0.0:9102' --workers 1 erddap_metrics.api.run:__hug_wsgi__

# then open a browser to http://localhost:9102/
```

## How it works

A process runs periodically and scrapes information from `/status.html` (and optionally the All Datasets dataset)
for each ERDDAP server, and publishes the results.

You can configure a single metrics instance that inspects multiple ERDDAP servers.

The results are available via a Prometheus (https://prometheus.io/) metrics endpoint, which you can plug in to Grafana (https://grafana.com/) 
to view metrics over time and create alerts. 
The results are available via a REST API so you can integrate it into custom dashboards and applications. 

## Tutorial: setting up erddap-metrics with Prometheus and Grafana

See tutorial in the docs: [Tutorial: setting up erddap-metrics with Prometheus and Grafana](https://github.com/axiom-data-science/erddap-metrics/blob/master/docs/tutorial.md)

## Configuration (`settings.yml`)

`erddap_regions` contains a list of ERDDAP servers you want to monitor.

Each region has the following settings:

* `name` -- human readable label, e.g., `"aoos"`
* `base_url` -- root URL, e.g., `"http://erddap.aoos.org/erddap"`
* `enable_dataset_metrics` -- whether or not to collect metrics for individual ERDDAP datasets
    * set to `"true"` or `"false"` (default: `false`)
* `dataset_metrics_max_age_seconds` -- how far back to collect individual metrics
    * e.g., `604800` for the past 7 days
    * for datasets old than this, the app won't track individual metrics
    * generally, you only want to alert on active datasets going out of date, so there's no reason to monitor and store historic datasets, and limiting the number of metrics makes things more efficient

## Running locally

### Setup

First, create a local config file:

```
# Copy example settings to settings.yml
# Update with whatever servers you want to test with 
cp settings.yml.example settings.yml
```

### Run
 
#### Command line

Conda env:
```
# create
conda create -y -c conda-forge  -n erddap_metrics python=3.8 --file requirements.txt --file requirements-dev.txt

# enable
source activate erddap_metrics

# update
conda install -y -c conda-forge  --file requirements.txt --file requirements-dev.txt
```

Run with:
```
# run hug
hug -p 9102 -f erddap_metrics/api/run.py
# or run gunicorn
gunicorn --bind '0.0.0.0:9102' --workers 1 erddap_metrics.api.run:__hug_wsgi__
```

Test with:

```
pytest
```

Then open a browser to http://localhost:9102/

#### Docker

```
# Build
docker build -t erddap-metrics .

# Run
docker run --rm --name erddap-metrics \
   -p 9102:9102  \
   -v $(pwd)/settings.yml:/app/settings.yml \
 erddap-metrics gunicorn --bind '0.0.0.0:9102' --workers 1 erddap_metrics.api.run:__hug_wsgi__
```


# TODOs

* Dev
  * External review
* Features
  * Expose list of regions via rest api
