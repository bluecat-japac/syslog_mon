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


def get_alarm_host_name():
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    config_file = os.path.join(basedir, "Config", "config.ini")
    config = configparser.ConfigParser()
    config.read(config_file)
    alm_hostname = config.get("SCHEDULER_CONFIG", "VM_HOST_NAME")
    return alm_hostname


def get_ntp_config_data():
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    config_file = os.path.join(basedir, "Config", "config.ini")
    config = configparser.ConfigParser()
    config.read(config_file)
    interval = config.getint("NTP_CONFIG", "INTERVAL")
    threshold = config.get("NTP_CONFIG", "THRESHOLD")
    bdds_server = config.get("NTP_CONFIG", "BDDS_SERVER")
    return interval, threshold, bdds_server


def get_interval_data():
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    config_file = os.path.join(basedir, "Config", "config.ini")
    config = configparser.ConfigParser()
    config.read(config_file)
    interval = config.getint("TCP_LIMIT_EXCEED_CONFIG", "INTERVAL")
    return interval


def read_file(path):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return f.read()