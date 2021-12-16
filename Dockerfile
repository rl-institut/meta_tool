FROM python:3.8.0-slim

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        make \
        gcc

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN apt-get remove -y --purge make gcc build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY ./ /app
WORKDIR /app

CMD gunicorn meta_tool.wsgi --bind 0.0.0.0:80 --chdir=/app