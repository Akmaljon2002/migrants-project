FROM python:3.12.4-slim

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -m nonroot
USER nonroot

COPY . /code
WORKDIR /code

EXPOSE 8080

CMD gunicorn --bind 0.0.0.0:${PORT:-8080} --access-logfile - core.wsgi:application --workers 3 --timeout 120

