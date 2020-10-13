# erddap-metrics

Provides ERDDAP metrics and status, via a REST API and Prometheus metrics endpoint.

## How it works

A process runs periodically and scrapes the `/status.html` for each ERDDAP server, and publishes the results.

You can configure a single metrics instance that inspects multiple ERDDAP servers.

The results are available via a Prometheus (https://prometheus.io/) metrics endpoint, which you can plug in to Grafana (https://grafana.com/) 
to view metrics over time and create alerts. 
The results are available via a REST API so you can integrate it into custom dashboards and applications. 

## Tutorial: setting up erddap-metrics with Prometheus and Grafana

See tutorial in the docs: [Tutorial: setting up erddap-metrics with Prometheus and Grafana](https://github.com/axiom-data-science/erddap-metrics/blob/master/docs/tutorial.md)

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
conda create -y -c conda-forge  -n erddap_metrics python=3.8 --file requirements.txt --file requirements-test.txt

# enable
source activate erddap_metrics

# update
conda install -y -c conda-forge  --file requirements.txt --file requirements-test.txt
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

* Add LICENSE
* Travis-CI pipeline
* Publish to Docker Hub
* Compare to [ioos-python-package-skeleton](https://github.com/ioos/ioos-python-package-skeleton) / Filipe review
* Expose list of regions via rest api
