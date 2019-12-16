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


import atexit
import os
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from config import logger, LOG_PRIORITY
from .common import get_ntp_config_data
from .common import get_alarm_host_name

executors = {
    "default": ThreadPoolExecutor(20),
    "processpool": ProcessPoolExecutor(5)
}

job_defaults = {
    "coalesce": False,
    "max_instances": 3
}

scheduler = BackgroundScheduler()
scheduler.configure(executors=executors, job_defaults=job_defaults)


NtpClocksUnsynchronized = {}
interval, threshold, bdds_servers = get_ntp_config_data()
alm_hostname = get_alarm_host_name()


def set_or_clear_alarm_ntp_clock_unsynchronized(case, source, target):
    key = "{0}_{1}".format(source, target)
    if case.lower() == "set":
        if key in NtpClocksUnsynchronized.keys():
            return None, None
        NtpClocksUnsynchronized.update({key: {}})
        return "set", key
    elif case.lower() == "clear":
        if key in NtpClocksUnsynchronized.keys():
            del NtpClocksUnsynchronized[key]
            return "clear", key
        return None, None
    return None, None


def check_time_gap():
    if bdds_servers:
        for bdds_server in bdds_servers.split(','):
            cmd = "ntpq -p -n {0}".format(bdds_server)
            out = os.popen(cmd).read()
            if out and "No association ID's returned" not in out:
                ntp_offsets = {}
                ntp_servers = out.split('\n')
                for idx in range(2, len(ntp_servers)-1):
                    server_ip = ntp_servers[idx].split()[0]
                    offset = ntp_servers[idx].split()[8]
                    if not server_ip[0].isalnum() or server_ip[0] == 'x' or server_ip[0] == 'o':
                        server_ip = server_ip[1:]
                    ntp_offsets[server_ip] = float(offset)
                try:
                    for server in ntp_offsets:
                        if abs(ntp_offsets[server]) > float(threshold):
                            case = "set"
                        else:
                            case = "clear"
                        cond, keypair = set_or_clear_alarm_ntp_clock_unsynchronized(case, bdds_server, server)
                        logger.info("NtpClocksUnsynchronized-case: {0} - {1}".format(cond, keypair))
                        if cond is not None and keypair is not None:
                            basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
                            snmpv3_file_path = os.path.join(basedir, "Snmp", "snmpv3.py")
                            os.system('python "{0}" "{1}" "{2}" "{3}" "{4}" "{5}" "{6}"'.format(snmpv3_file_path, cond, LOG_PRIORITY['err'],
                                       keypair, "Time gap between BDDS {} and NTP server {} has changed: {}".format(bdds_server,server,ntp_offsets[server]), "NtpClocksUnsynchronized", alm_hostname))
                            logger.info("NtpClocksUnsynchronized-send successfully:{0} - {1}".format(cond, keypair))
                except Exception as ex:
                    logger.error(ex)
            else:
                logger.error("Execute command 'ntpq -p -n {0}' failed.".format(bdds_server))
    else:
        logger.error("The bdds list is empty")


scheduler.add_job(check_time_gap, trigger='interval', minutes=interval, id='ntp')
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
