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


import re
import datetime
import os
from .alarm_regex_common import *
from config import logger, LOG_PRIORITY
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from common import get_interval_data


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
# Interval time (in minutes) before sending clear alarm
interval = get_interval_data()


LOADCONFIGURATIONFAILED = "LoadConfigurationFailed"
LOADZONEFAILED = "LoadZoneFailed"
TSIGBADTIME = "TsigBadTime"
NETWORKINTERFACEDOWN = "NetworkInterfaceDown"
STORAGEREADONLY = "StorageReadOnly"
ZONETRANSFERFAILED = "ZoneTransferFailed"
TCPCONNECTIONLIMITEXCEEDED = "TcpConnectionLimitExceeded"

key_pair = {
    LOADCONFIGURATIONFAILED: {
    },
    LOADZONEFAILED: {
    },
    TSIGBADTIME: {
    },
    NETWORKINTERFACEDOWN: {
    },
    STORAGEREADONLY: {
    },
    ZONETRANSFERFAILED: {
    },
    TCPCONNECTIONLIMITEXCEEDED: {
    }
}


def monitor_alarm(host, filter_name, message):
    """

    :param host: source
    :param filter_name: filter name
    :param message: error message
    :return:
        "set" or "clear", keypair, error_type
    """
    # Mixed message
    logger.debug("Alarm_management monitor_alarm:{0} - {1} - {2}".format(host, filter_name, message))
    try:
        filter_split = filter_name.split('_')
        error_type = filter_split[0]
        case = filter_split[1]
        if error_type.lower() == LOADCONFIGURATIONFAILED.lower():
            return set_or_clear_alarm_with_key_source(error_type, case, host, message) + (host,)
        elif error_type.lower() == LOADZONEFAILED.lower():
            return set_or_clear_alarm_with_key_source_zone(error_type, case, host, message) + (host,)
        elif error_type.lower() == TSIGBADTIME.lower():
            return set_or_clear_alarm_with_key_source_target(error_type, case, host, message) + (host,)
        elif error_type.lower() == NETWORKINTERFACEDOWN.lower():
            return set_or_clear_alarm_with_key_source_interface(error_type, case, host, message) + (host,)
        elif error_type.lower() == STORAGEREADONLY.lower():
            return set_or_clear_alarm_with_key_source(error_type, case, host, message) + (host,)
        elif error_type.lower() == ZONETRANSFERFAILED.lower():
            return set_or_clear_alarm_with_key_source_target(error_type, case, host, message) + (host,)
        elif error_type.lower() == TCPCONNECTIONLIMITEXCEEDED.lower():
            return set_or_clear_alarm_with_key_source(error_type, case, host, message) + (host,)
        # if does not set/clear return None, None, None
        logger.debug("Alarm_management monitor_alarm:None of error type in list {0} - {1} - {2}".format(host, filter_name, message))
        return None, None, None, host
    except Exception as ex:
        logger.error(
            "Alarm_management monitor_alarm:{0}".format(ex)
        )
        return None, None, None, host


def set_or_clear_alarm_with_key_source(error_type, case, host, message):
    """

    :param error_type: LoadConfigurationFailed, StorageReadOnly..
    :param case: set/clear
    :param host: in ip address for example: 172.21.3.14
    :param message: in string
    :return:
          "set" or "clear", keypair, error_type
    """
    logger.debug("Alarm_management with_key_source: {0} - {1} - {2} - {3}".format(error_type, case, host, message))
    try:
        key = host
        if case.lower() == "set":
            if error_type.lower() == TCPCONNECTIONLIMITEXCEEDED.lower():
                return set_tcp_connection_limit_exceeded(key, error_type, host)
            else:
                return set_alarm(key, error_type)
        elif case.lower() == "clear":
            if error_type.lower() == LOADCONFIGURATIONFAILED.lower():
                return clear_with_source(key, error_type)
            elif error_type.lower() == STORAGEREADONLY.lower():
                return clear_with_source(key, error_type)
        elif case.lower() == "forceclear":
            return "forceclear", key, error_type
        return None, None, None
    except Exception as ex:
        logger.error(
            "Alarm_management set-clear key_source: {0}".format(ex)
        )
        return None, None, None


def set_or_clear_alarm_with_key_source_target(error_type, case, host, message):
    """

    :param error_type: TsigBadTime, ZoneTransferFailed
    :param case: set/clear
    :param host: in ip address for example: 172.21.3.14
    :param message: in string
    :return:
        "set" or "clear", keypair, error_type
    """
    logger.debug("Alarm_management with_key_source_target: {0} - {1} - {2} - {3}".format(error_type, case, host, message))
    try:
        pattern = REG_TARGET_STRING_IP
        target_pattern = REG_TARGET_IP
        value_matched = re.search(pattern, message).group()
        target = re.search(target_pattern, value_matched).group()
        key = "{0}_{1}".format(host, target)
        if case.lower() == "set":
            if error_type.lower() == ZONETRANSFERFAILED.lower():
                return set_zone_transfer(key, error_type, message)
            else:
                return set_alarm(key, error_type)
        elif case.lower() == "clear":
            if error_type.lower() == TSIGBADTIME.lower():
                return clear_with_source(key, error_type)
            elif error_type.lower() == ZONETRANSFERFAILED.lower():
                return clear_zone_transfer(key, error_type, message)
        return None, None, None
    except Exception as ex:
        logger.error(
            "Alarm_management set-clear key_source_target: {0}".format(ex)
        )
        return None, None, None


def set_or_clear_alarm_with_key_source_zone(error_type, case, host, message):
    """

    :param error_type: LoadZoneFailed
    :param case: set/clear
    :param host: in ip address for example: 172.21.3.14
    :param message: in string
    :return:
        "set" or "clear", keypair, error_type
    """
    logger.debug("Alarm_management with_key_source_zone: {0} - {1} - {2} - {3}".format(error_type, case, host, message))
    try:
        pattern = REG_ZONE_STRING
        zone_pattern = REG_ZONE
        value = re.search(pattern, message)
        if value:
            value_matched = value.group()
            target = re.search(zone_pattern, value_matched).group()
            key = "{0}_{1}".format(host, target)
            if case.lower() == "set":
                return set_alarm(key, error_type)
            elif case.lower() == "clear":
                if error_type.lower() == LOADZONEFAILED.lower():
                    return clear_with_source(key, error_type)
        return None, None, None
    except Exception as ex:
        logger.error(
            "Alarm_management set-clear key_source_zone: {0}".format(ex)
        )
        return None, None, None


def set_or_clear_alarm_with_key_source_interface(error_type, case, host, message):
    """

    :param error_type: NetworkInterfaceDown
    :param case: set/clear
    :param host: in ip address for example: 172.21.3.14
    :param message: in string
    :return:
         "set" or "clear", keypair, error_type
    """
    logger.debug("Alarm_management with_key_source_interface: {0} - {1} - {2} - {3}".format(error_type, case, host, message))
    try:
        if case.lower() == "set":
            pattern = REG_INTERFACE_STRING_DOWN
            interface_pattern = REG_INTERFACE
            interface_string_matched = re.search(pattern, message).group()
            interface_matched = re.search(interface_pattern, interface_string_matched).group().replace(",", "")
            key = "{0}_{1}".format(host, interface_matched)
            return set_alarm(key, error_type)
        elif case.lower() == "clear":
            if error_type.lower() == NETWORKINTERFACEDOWN.lower():
                return clear_network_interface(host, error_type, message)
        return None, None, None
    except Exception as ex:
        logger.error(
            "Alarm_management set-clear key_source_interface: {0}".format(ex)
        )
        return None, None, None


def set_zone_transfer(key, error_type, message):
    if key in key_pair[error_type].keys():
        return None, None, None
    zone_string_pattern = REG_ZONE_STRING
    zone_pattern = REG_ZONE
    zone_string_matched = re.search(zone_string_pattern, message).group()
    zone_matched = re.search(zone_pattern, zone_string_matched).group()
    key_pair[error_type].update({key: zone_matched})
    return "set", key, error_type


def set_alarm(key, error_type):
    if key in key_pair[error_type].keys():
        return None, None, None
    key_pair[error_type].update({key: {}})
    return "set", key, error_type


def set_tcp_connection_limit_exceeded(key, error_type, host):
    if key in key_pair[error_type].keys():
        update_clear_tcp_connection_limit_exceeded(key)
        return None, None, None
    key_pair[error_type].update({key: str(datetime.datetime.now())})
    add_clear_tcp_connection_limit_exceeded(key, error_type, host)
    return "set", key, error_type


def clear_with_source(key, error_type):
    if key in key_pair[error_type].keys():
        return clear_alarm(error_type, key)
    return None, None, None


def clear_network_interface(host, error_type, message):
    # Get interface
    pattern_interface = REG_INTERFACE_STRING_UP
    regex_obj_interface = re.compile(pattern_interface)
    val_match_interface = regex_obj_interface.search(message, 0)
    interface = val_match_interface.group(0).split()[4]

    key = "{0}_{1}".format(host, interface)
    if key in key_pair[error_type].keys():
        return clear_alarm(error_type, key)
    return None, None, None


def clear_zone_transfer(key, error_type, message):
    # Get zone
    pattern_zone = REG_ZONE_STRING
    regex_obj_zone = re.compile(pattern_zone)
    val_match_zone = regex_obj_zone.search(message, 0)
    raw_value = val_match_zone.group(0).split()[2]
    zone = raw_value[1:]

    try:
        value = key_pair[error_type].get(key, None)
        if value and (value.lower() == zone.lower()):
            return clear_alarm(error_type, key)
        return None, None, None
    except KeyError as key_error:
        logger.error(
            "Alarm_management clear_zone_transfer: {0}".format(key_error)
        )
        return None, None, None


def add_clear_tcp_connection_limit_exceeded(key, error_type, host):
    """
    STATE_STOPPED   0
    STATE_RUNNING   1
    STATE_PAUSED    2
    """
    # Check scheduler is running or not
    if scheduler.state == 1:
        pass
    elif scheduler.state == 2:
        scheduler.resume()
    else:
        scheduler.start()

    end_date = datetime.datetime.now() + datetime.timedelta(minutes=interval)
    scheduler.add_job(tcp_connection_limit_exceeded_job, kwargs={"key": key, "error_type": error_type, "host": host}, id=key,
                      run_date=end_date)


def update_clear_tcp_connection_limit_exceeded(key):
    end_date = datetime.datetime.now() + datetime.timedelta(minutes=interval)
    scheduler.reschedule_job(key, run_date=end_date)


def tcp_connection_limit_exceeded_job(key, error_type, host):
    # Send a message to the target service
    if key in key_pair[error_type].keys():
        case, key, error_type = clear_alarm(error_type, key)
        filter_name = "{0}_{1}".format(error_type, case)
        logger.info("Alarm_management tcp_connection_limit_exceeded clear:{0} - {1} - {2}".format(case, key, filter_name))
        try:
            basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            snmpv3_file_path = os.path.join(basedir, "Snmp", "snmpv3.py")
            message = "No error relating to TCP connections limit exceeded after waiting for {0} minutes.".format(interval)
            os.system(
                'python "{0}" "{1}" "{2}" "{3}" "{4}" "{5}" "{6}"'.format(snmpv3_file_path, case, LOG_PRIORITY["notice"],
                                                                    key, message, error_type, host))
            logger.info("Monitoring send successfully:{0} - {1} - {2}".format(case, key, filter_name))
        except Exception as ex:
            logger.error(
                "Monitoring send failed:{0}".format(ex)
            )


def clear_alarm(error_type, key):
    try:
        del key_pair[error_type][key]
    except Exception as ex:
        logger.error(
            "Alarm_management clear_alarm: {0}".format(ex)
        )
        return None, None, None
    return "clear", key, error_type


scheduler.start()

