FROM apache/airflow:3.1.2
USER root
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
USER airflow
RUN pip install --no-cache-dir apache-airflow-providers-postgres
