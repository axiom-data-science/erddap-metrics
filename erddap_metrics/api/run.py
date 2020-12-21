#!python
# coding=utf-8

import hug
from hug.middleware import CORSMiddleware

from erddap_metrics.api import prom
from erddap_metrics.api import rest

hug.API(__name__).http.add_middleware(CORSMiddleware(hug.API(__name__), allow_origins=["*"]))

hug.API(__name__).extend(rest, '/rest')
hug.API(__name__).extend(prom, '/metrics')


@hug.get('/')
def get_help(request):
    url_prefix = request.url[:-1]
    return {
        'documentation': hug.API(__name__).http.documentation(prefix=url_prefix)
    }
