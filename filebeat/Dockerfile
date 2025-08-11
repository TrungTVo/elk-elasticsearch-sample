# Use the official Filebeat base image from Elastic
FROM docker.elastic.co/beats/filebeat:9.1.1

# Run as root user
USER root

# Install Vim editor and ping command
# RUN apt-get update && \
#     apt-get install -y vim && \
#     apt-get install -y iputils-ping

# Set the working directory
WORKDIR /usr/share/filebeat

# Expose ports 5044
EXPOSE 5044

# Copy files over
COPY ../filebeat/filebeat.yml ./
COPY ../workspace_data/ ./workspace_data/