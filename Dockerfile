FROM continuumio/miniconda3:4.9.2

# Install requirements
COPY requirements*.txt /tmp/
RUN  /opt/conda/bin/conda install -y -c conda-forge -c axiom-data-science \
        python=3.8 --file /tmp/requirements.txt --file /tmp/requirements-dev.txt \
     && /opt/conda/bin/conda  clean -a -y

# Copy app contents
WORKDIR /app
COPY . /app
