ARG IMAGE=syslog_monitoring:<tag>
FROM $IMAGE
RUN   ln -s / /rootlink && \
      rm -rf /usr/lib/apt/methods/mirror* \
            /etc/alternatives/cpp \
            /usr/bin/cpp \
            /usr/lib/cpp  \
            /lib/cpp \
            /usr/share/doc/cpp \
            /var/lib/dpkg/alternatives/cpp
FROM scratch
COPY --from=0 /rootlink/ /
RUN rm -rf /rootlink
ENV PYTHONPATH /etc/syslog-ng/syslog_monitoring
CMD  ["./start.sh"]