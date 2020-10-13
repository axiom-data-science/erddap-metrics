from setuptools import setup, find_packages


def version():
    with open('VERSION') as f:
        return f.read().strip()


def readme():
    with open('README.md') as f:
        return f.read().strip()


reqs = [line.strip() for line in open('requirements.txt') if not line.startswith('#')]

setup(
    name                = 'erddap-metrics',
    version             = version(),
    description         = 'Provides ERDDAP metrics and status, via a REST API and Prometheus metrics endpoint.',
    long_description    = readme(),
    license             = 'Apache',
    author              = "Jessica Austin",
    author_email        = "jessica@axds.co",
    url                 = "https://github.com/axiom-data-science/erddap-metrics",
    packages            = find_packages(),
    install_requires    = reqs,
    classifiers         = [
        "Development Status :: 3 - Alpha",
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics'
    ]
)
