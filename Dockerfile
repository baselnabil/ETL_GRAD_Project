FROM apache/airflow:2.7.1

USER root

COPY requirements.txt /requirements.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        default-jdk \
        procps \
        libpq-dev \
        curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
ENV PATH $JAVA_HOME/bin:$PATH


RUN mkdir -p /opt/spark/jars && \
    chmod -R 777 /opt/spark/jars

RUN curl -L https://jdbc.postgresql.org/download/postgresql-42.6.0.jar -o /tmp/postgresql-42.6.0.jar && \
    mv /tmp/postgresql-42.6.0.jar /opt/spark/jars/postgresql-42.6.0.jar

USER airflow
ENV PATH="$PATH:/home/basel/main/Grad_proj"

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt