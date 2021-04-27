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

import json
from config import *
from Alarm import alarm_management, common

basedir = os.path.dirname(os.path.abspath(__file__))


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

        state_file = os.path.join(basedir, "current_state")
        forceclear_file = os.path.join(basedir, "forceclear")
        state_data = common.read_file(state_file)
        if state_data:
            state = json.loads(state_data)
            logger.info("Load current state from file: {}".format(state))
            alarm_management.key_pair = state
            os.remove(state_file)

        forceclear_data = common.read_file(forceclear_file)
        if forceclear_data:
            logger.info("forceclear is existed: {}".format(forceclear_file))
            logger.info("forceclear file data : {}".format(forceclear_data))
            cond, msg_level, keypair, msg, err_type, host = forceclear_data.split('|')
            self._send_trap(cond, msg_level, keypair, msg, err_type, host)
            os.remove(forceclear_file)

        return True

    def close(self):
        """Close the connection to the target  service"""
        logger.info("Monitoring:{0}".format("Close"))
        state_file = os.path.join(basedir, "current_state")
        state = json.dumps(alarm_management.key_pair)
        with open(state_file, "w+") as f:
            logger.info("Create state file: {}".format(state_file))
            logger.info("Save current alarm state to file before restart syslog-ng: {}".format(state))
            f.write(state)
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
        if cond == "forceclear":
            forceclear = os.path.join(basedir, "forceclear")
            data = "{0}|{1}|{2}|{3}|{4}|{5}".format(cond, msg["LEVEL"], keypair, msg["MESSAGE"], err_type, host)
            with open(forceclear, "w+") as forceclear_file:
                logger.info("Create forceclear file: {}".format(forceclear))
                forceclear_file.write(data)
                forceclear_file.seek(0)
                logger.info("Write data to forceclear file: {}".format(data))
        else:
            try:
                self._send_trap(cond, msg["LEVEL"], keypair, msg["MESSAGE"], err_type, host)
            except Exception as ex:
                logger.error(
                    "Monitoring send failed:{}".format(ex)
                )
        return True

    def _send_trap(self, cond, msg_level, keypair, msg, err_type, host):
        logger.info("Send trap: {0}|{1}|{2}|{3}|{4}|{5}".format(cond, msg_level, keypair, msg, err_type, host))
        snmpv3_file_path = os.path.join(basedir, "Snmp", "snmpv3.py")
        os.system('python "{0}" "{1}" "{2}" "{3}" "{4}" "{5}" "{6}"'.format(snmpv3_file_path, cond,
                                                                            LOG_PRIORITY[msg_level], keypair,
                                                                            msg, err_type, host))