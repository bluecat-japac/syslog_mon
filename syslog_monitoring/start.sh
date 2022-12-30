#!/usr/bin/env bash

kill_syslog_ng() {
   echo "Start kill syslog-ng ..."
   pkill syslog-ng
   sleep 10
}
trap "echo SIGINT; kill_syslog_ng; exit"  SIGINT
trap "echo SIGTERM; kill_syslog_ng; exit" SIGTERM
echo Starting script

echo "Restart cron service if it not running ..."

if service cron status | grep 'is running'
then
   echo "Service cron is running";
else
   service cron start
fi

echo "Run syslog-ng in foreground ..."

syslog-ng --process-mode=foreground --no-caps &

wait -n
