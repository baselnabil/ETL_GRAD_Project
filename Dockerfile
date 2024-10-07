FROM apache/airflow:2.10.2

USER root

COPY requirements.txt /requirements.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        default-jre \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME

USER airflow

# Install PySpark and JDBC dependencies
RUN pip install --no-cache-dir -r /requirements.txt