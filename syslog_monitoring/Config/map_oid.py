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

MAP_OID = {
    "TestQueryFailed": {
        "OID":"1.3.6.1.4.1.13315.6.1.2.0.1",
        "bcnSyslogMonAlarmCond": "1.3.6.1.4.1.13315.6.1.2.1.1.0",
        "bcnSyslogMonAlarmSeverity": "1.3.6.1.4.1.13315.6.1.2.1.2.0",
        "bcnSyslogMonKeyPair": "1.3.6.1.4.1.13315.6.1.2.1.3.0",
        "bcnSyslogMonHostInfo": "1.3.6.1.4.1.13315.6.1.2.1.4.0",
        "bcnSyslogMonAlarmMsg": "1.3.6.1.4.1.13315.6.1.2.1.5.0"
        
    },
    "LoadConfigurationFailed": {
        "OID":"1.3.6.1.4.1.13315.6.1.2.0.2",
        "bcnSyslogMonAlarmCond": "1.3.6.1.4.1.13315.6.1.2.1.1.0",
        "bcnSyslogMonAlarmSeverity": "1.3.6.1.4.1.13315.6.1.2.1.2.0",
        "bcnSyslogMonKeyPair": "1.3.6.1.4.1.13315.6.1.2.1.3.0",
        "bcnSyslogMonHostInfo": "1.3.6.1.4.1.13315.6.1.2.1.4.0",
        "bcnSyslogMonAlarmMsg": "1.3.6.1.4.1.13315.6.1.2.1.5.0"
    },
    "TsigBadTime": {
        "OID":"1.3.6.1.4.1.13315.6.1.2.0.3",
        "bcnSyslogMonAlarmCond": "1.3.6.1.4.1.13315.6.1.2.1.1.0",
        "bcnSyslogMonAlarmSeverity": "1.3.6.1.4.1.13315.6.1.2.1.2.0",
        "bcnSyslogMonKeyPair": "1.3.6.1.4.1.13315.6.1.2.1.3.0",
        "bcnSyslogMonHostInfo": "1.3.6.1.4.1.13315.6.1.2.1.4.0",
        "bcnSyslogMonAlarmMsg": "1.3.6.1.4.1.13315.6.1.2.1.5.0"
    },
    "StorageReadOnly":{
        "OID":"1.3.6.1.4.1.13315.6.1.2.0.4",
        "bcnSyslogMonAlarmCond": "1.3.6.1.4.1.13315.6.1.2.1.1.0",
        "bcnSyslogMonAlarmSeverity": "1.3.6.1.4.1.13315.6.1.2.1.2.0",
        "bcnSyslogMonKeyPair": "1.3.6.1.4.1.13315.6.1.2.1.3.0",
        "bcnSyslogMonHostInfo": "1.3.6.1.4.1.13315.6.1.2.1.4.0",
        "bcnSyslogMonAlarmMsg": "1.3.6.1.4.1.13315.6.1.2.1.5.0"
    },
    "ZoneTransferFailed": {
        "OID":"1.3.6.1.4.1.13315.6.1.2.0.5",
        "bcnSyslogMonAlarmCond": "1.3.6.1.4.1.13315.6.1.2.1.1.0",
        "bcnSyslogMonAlarmSeverity": "1.3.6.1.4.1.13315.6.1.2.1.2.0",
        "bcnSyslogMonKeyPair": "1.3.6.1.4.1.13315.6.1.2.1.3.0",
        "bcnSyslogMonHostInfo": "1.3.6.1.4.1.13315.6.1.2.1.4.0",
        "bcnSyslogMonAlarmMsg": "1.3.6.1.4.1.13315.6.1.2.1.5.0"
    },
    "TcpConnectionLimitExceeded": {
        "OID":"1.3.6.1.4.1.13315.6.1.2.0.6",
        "bcnSyslogMonAlarmCond": "1.3.6.1.4.1.13315.6.1.2.1.1.0",
        "bcnSyslogMonAlarmSeverity": "1.3.6.1.4.1.13315.6.1.2.1.2.0",
        "bcnSyslogMonKeyPair": "1.3.6.1.4.1.13315.6.1.2.1.3.0",
        "bcnSyslogMonHostInfo": "1.3.6.1.4.1.13315.6.1.2.1.4.0",
        "bcnSyslogMonAlarmMsg": "1.3.6.1.4.1.13315.6.1.2.1.5.0"
    },
    "LoadZoneFailed":{
        "OID": "1.3.6.1.4.1.13315.6.1.2.0.7",
        "bcnSyslogMonAlarmCond":"1.3.6.1.4.1.13315.6.1.2.1.1.0",
        "bcnSyslogMonAlarmSeverity": "1.3.6.1.4.1.13315.6.1.2.1.2.0",
        "bcnSyslogMonKeyPair": "1.3.6.1.4.1.13315.6.1.2.1.3.0",
        "bcnSyslogMonHostInfo": "1.3.6.1.4.1.13315.6.1.2.1.4.0",
        "bcnSyslogMonAlarmMsg": "1.3.6.1.4.1.13315.6.1.2.1.5.0"
    },
    "NtpClocksUnsynchronized":{
        "OID": "1.3.6.1.4.1.13315.6.1.2.0.8",
        "bcnSyslogMonAlarmCond": "1.3.6.1.4.1.13315.6.1.2.1.1.0",
        "bcnSyslogMonAlarmSeverity": "1.3.6.1.4.1.13315.6.1.2.1.2.0",
        "bcnSyslogMonKeyPair": "1.3.6.1.4.1.13315.6.1.2.1.3.0",
        "bcnSyslogMonHostInfo": "1.3.6.1.4.1.13315.6.1.2.1.4.0",
        "bcnSyslogMonAlarmMsg": "1.3.6.1.4.1.13315.6.1.2.1.5.0"
    },
    "NetworkInterfaceDown":{
        "OID": "1.3.6.1.4.1.13315.6.1.2.0.9",
        "bcnSyslogMonAlarmCond":"1.3.6.1.4.1.13315.6.1.2.1.1.0",
        "bcnSyslogMonAlarmSeverity": "1.3.6.1.4.1.13315.6.1.2.1.2.0",
        "bcnSyslogMonKeyPair": "1.3.6.1.4.1.13315.6.1.2.1.3.0",
        "bcnSyslogMonHostInfo": "1.3.6.1.4.1.13315.6.1.2.1.4.0",
        "bcnSyslogMonAlarmMsg": "1.3.6.1.4.1.13315.6.1.2.1.5.0"

    }
}