FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONPATH /etc/syslog-ng/syslog_monitoring

RUN apt-get update && \
    apt-get install -y gnupg2 syslog-ng-core syslog-ng python-pip snmp snmpd && \
    mv /etc/syslog-ng/syslog-ng.conf /etc/syslog-ng/syslog-ng-backup.conf

COPY syslog-ng.conf /etc/syslog-ng/syslog-ng.conf
RUN mkdir /var/log/mon-app /var/log/mon-app/fw-log /var/log/mon-app/filter-log && \
    mkdir /usr/share/syslog-ng/include/scl/syslog_mon/
COPY . /etc/syslog-ng/syslog_monitoring
COPY filters.conf /usr/share/syslog-ng/include/scl/

RUN \
    pip install wheel && \
    pip install -r /etc/syslog-ng/syslog_monitoring/requirements.txt && \
    apt-get install -y tzdata && \
    dpkg-reconfigure tzdata && \
    apt-get install ntp -y

CMD ["syslog-ng", "--process-mode=foreground"]
