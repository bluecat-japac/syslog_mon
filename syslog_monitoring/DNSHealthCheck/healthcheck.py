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
import re
import dns.message
import dns.query
import dns.flags
import dns.name
from .port import check_DNS_port_open
from .common import get_config_data
from .constants import DNS_QUERY_TIMEOUT


def get_name_servers():
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))
    name_servers = []
    with open("{}/{}".format(basedir, "/Config/resolv.conf"), "r") as rconfig:
        lines = rconfig.readlines()
        for line in lines:
            regex_ipv6 = '''(?:^|(?<=\s))(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|
            ([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|
            ([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|
            ([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|
            [0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|
            fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|
            1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|
            ([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|
            (2[0-4]|1{0,1}[0-9]){0,1}[0-9]))(?=\s|$)'''
            ip = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line) if '.' in line else re.search(regex_ipv6, line)
            if ip:
                name_servers.append(ip.group(0))
            if 'sourceIP' in line:
                name_servers.append(line.strip())
    return name_servers


def health_check_dns_server(name_servers):
    _, domain_name, RDCLASS, _ = get_config_data()
    dns_domain = dns.name.from_text(domain_name)
    if not dns_domain.is_absolute():
        dns_domain = dns_domain.concatenate(dns.name.root)
    req = dns.message.make_query(dns_domain, dns.rdatatype.ANY)
    req.flags != dns.flags.AD
    req.find_rrset(req.additional, dns.name.root, RDCLASS, dns.rdatatype.OPT, create=True, force_unique=True)
    source_ipv4, source_ipv6 = get_source_ip(name_servers)
    result_health_check_dns_server = []
    for name_server in name_servers:
        status = False
        if 'sourceIP' not in name_server:
            if check_DNS_port_open(domain_name, name_server):
                try:
                    source_ip = source_ipv6 if ':' in name_server else source_ipv4
                    dns.query.udp(req, name_server, DNS_QUERY_TIMEOUT, source=source_ip)
                    status = True
                except dns.exception.Timeout:
                    pass
            result_health_check_dns_server.append({
                "name_server": name_server,
                "status": status
            })
    return result_health_check_dns_server


def get_source_ip(name_servers):
    loopback_ipv6 = loopback_ipv4 = None
    for name_server in name_servers:
        if 'sourceIPv4' in name_server:
            loopback_ipv4 = name_server.split('sourceIPv4-')[1]
        elif 'sourceIPv6' in name_server:
            loopback_ipv6 = name_server.split('sourceIPv6-')[1]
    return loopback_ipv4, loopback_ipv6
