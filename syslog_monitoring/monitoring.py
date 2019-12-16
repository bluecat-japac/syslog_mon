# Copyright 2019 BlueCat Networks (USA) Inc. and its affiliates
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from config import *
from Alarm import alarm_management


class Monitoring(object):
    def __init__(self):
        """This method is called  at initialization  time
        Should return false if initialization fails"""
        self._is_opened = False

    def init(self, options):
        logger.info("Monitoring:{0}".format("Init"))
        import DNSHealthCheck
        import LogFileChecker
        import Alarm
        return True

    def open(self):
        """Open a connection to the target service
        Should  return  False if opening fails"""
        logger.info("Monitoring:{0}".format("Open"))
        self._is_opened = True
        return True

    def close(self):
        """Close the connection to the target  service"""
        logger.info("Monitoring:{0}".format("Close"))
        self._is_opened = False

    def is_opened(self):
        """Check if the connection to the target is able to receive messages"""
        return self._is_opened

    def deinit(self):
        """This method is called  at deinitialization time"""
        logger.info("Monitoring:{0}".format("Deinit"))

    def send(self, msg):
        """Send a message to the target service
        It should  return  True to indicate success, False will suspend the destination for a period  specified by the time"""
        logger.info(
            "Monitoring-syslog:{0} - LEVEL = {1} - HOST = {2} - MESSAGE = {3}".format(
                msg["DATE"], msg["LEVEL"], msg["HOST"], msg["MESSAGE"])
        )

        # Monitor alarm in order to set/clear
        cond, keypair, err_type, host = alarm_management.monitor_alarm(msg["HOST"], msg["FILTER_NAME"], msg["MESSAGE"])
        logger.info("Monitoring set-clear alarm:{0} - {1} - {2}".format(cond, keypair, msg["FILTER_NAME"]))
        if cond is None or keypair is None or err_type is None:
            return True
        try:
            basedir = os.path.dirname(os.path.abspath(__file__))  
            snmpv3_file_path = os.path.join(basedir, "Snmp", "snmpv3.py")
            os.system('python "{0}" "{1}" "{2}" "{3}" "{4}" "{5}" "{6}"'.format(snmpv3_file_path, cond, LOG_PRIORITY[msg["LEVEL"]], keypair, msg["MESSAGE"], err_type, host))
            logger.info("Monitoring send successfully:{0} - {1} - {2}".format(cond, keypair, msg["FILTER_NAME"]))
        except Exception as ex:
            logger.error(
                "Monitoring send failed:{}".format(ex)
            )    
        return True
