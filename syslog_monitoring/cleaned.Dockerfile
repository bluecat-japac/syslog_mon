# Support remove "cpp" and "mirror" in container

ARG IMAGE=syslog_monitoring:<tag>
FROM $IMAGE
RUN   ln -s / /rootlink && \
      rm -f /usr/lib/apt/methods/mirror* \
            /etc/alternatives/cpp \
            /usr/bin/cpp \
            /usr/lib/cpp  \
            /lib/cpp \
            /usr/share/doc/cpp \
            /var/lib/dpkg/alternatives/cpp
FROM scratch
COPY --from=0 /rootlink/ /
RUN rm -f /rootlink
ENV PYTHONPATH /etc/syslog-ng/syslog_monitoring
CMD  ["./start.sh"]