FROM ubuntu:bionic

ENV DEBIAN_FRONTEND noninteractive

# Update package list and install wget
RUN apt-get update && apt-get install -y wget gnupg2

# Get perforce packages
RUN wget -q http://package.perforce.com/perforce.pubkey -O - | apt-key add - && \
    echo "deb http://package.perforce.com/apt/ubuntu bionic release" > /etc/apt/sources.list.d/perforce.list && \
    apt update

RUN apt-get install -y helix-p4d curl

# Volumes for server roots and triggers
#VOLUME /opt/perforce/servers
#VOLUME /opt/perforce/triggers

EXPOSE 1666

# Add startup file and run it by default
COPY run.sh /
CMD ["/run.sh"]
