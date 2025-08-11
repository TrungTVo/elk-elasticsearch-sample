# Use the official Logstash base image from Elastic
FROM docker.elastic.co/logstash/logstash:9.1.1

# USER root

# Install Vim editor and ping command
# RUN apt-get update && \
#     apt-get install -y vim && \
#     apt-get install -y iputils-ping

# Set the working directory
WORKDIR /usr/share/logstash

RUN rm -f ./pipeline/logstash.conf

# Expose ports 5044 and 9600
EXPOSE 5044 9600

COPY ../logstash/config/ ./config/
COPY ../logstash/pipeline/ ./pipeline/
COPY ../workspace_data/ ./workspace_data/

# Command to run Logstash, select default configuration
# CMD ["bin/logstash", "-f", "/usr/share/logstash/pipeline/logstash2.conf"]