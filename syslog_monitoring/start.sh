#!/usr/bin/env bash

echo "Restart cron service if it not running ..."

if service cron status | grep 'is running'
then
   echo "Service cron is running";
else
   service cron start
fi

echo "Run syslog-ng in foreground ..."

syslog-ng --process-mode=foreground --no-caps
