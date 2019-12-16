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
from .common import get_config_data
from .healthcheck import (get_name_servers, health_check_dns_server)


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

TestQueryFailed = {

}

class ExecutorManager(object):

    def __init__(self):
        self.subscribers = dict()
        self.current_jobs = list()
        self.interval, _, _, _ = get_config_data()

    def register(self, who, job):
        self.subscribers[who] = job

    def unregister(self, who):
        del self.subscribers[who]

    def clear_up_job(self):
        remove_jobs = list(set(self.subscribers.keys()) - set(self.current_jobs))
        for job_id in remove_jobs:
            job = self.subscribers.get(job_id)
            self.unregister(job_id)
            job.remove_job(job_id)


manager = ExecutorManager()


def query_dns():
    interval, _, _, vm_host_name = get_config_data()
    if not interval:
        return
    name_servers = get_name_servers()
    data = health_check_dns_server(name_servers)
    logger.info(data)
    try:
        for server in data:
            source = vm_host_name
            if server["status"] == False:
                # SET ALARM
                case = "set"
            else:
                # CLEAR ALARM
                case = "clear"
            cond, keypair = set_or_clear_alarm_test_query_failed(case, source, server["name_server"])
            logger.info("DNSHealth-case: {0} - {1} - {2}".format(cond, keypair, "TestQueryFailed"))
            if cond is not None and keypair is not None:
                basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
                snmpv3_file_path = os.path.join(basedir, "Snmp", "snmpv3.py")
                os.system('python "{0}" "{1}" "{2}" "{3}" "{4}" "{5}" "{6}"'.format(snmpv3_file_path, cond, LOG_PRIORITY['err'],
                                                                        keypair,
                                                                        "DNSHealth: {0}".format(server["status"]),
                                                                        "TestQueryFailed", source))
                logger.info("DNSHealth-send successfully:{0} - {1} - {2}".format(cond, keypair, "TestQueryFailed"))
    except Exception as ex:
        logger.error(
            "DNSHealth-send:{}".format(ex)
        )


def set_or_clear_alarm_test_query_failed(case, source, target):
    key = "{0}_{1}".format(source, target)
    if case.lower() == "set":
        if key in TestQueryFailed.keys():
            return None, None
        TestQueryFailed.update({key:{}})
        return "set", key
    elif case.lower() == "clear":
        if key in TestQueryFailed.keys():
            del TestQueryFailed[key]
            return "clear", key
        return None, None
    return None, None


scheduler.add_job(query_dns, trigger='interval', minutes=manager.interval, id='manager')
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
