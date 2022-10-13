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

import os
import configparser
import socket


def get_config_data():
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    config_file = "{}{}".format(basedir, "/Config/config.ini")
    config = configparser.ConfigParser()
    config.read(config_file)
    interval = config.getint("SCHEDULER_CONFIG", "INTERVAL")
    domain_name = config.get("SCHEDULER_CONFIG", "DOMAIN")
    RDCLASS = config.getint("SCHEDULER_CONFIG", "RDCLASS")
    vm_host_name = config.get("SCHEDULER_CONFIG", "VM_HOST_NAME")
    return interval, domain_name, RDCLASS, vm_host_name


def check_ipv6(ip):
    try:
        socket.inet_pton(socket.AF_INET6, ip)
        return True
    except socket.error:
        return False