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


def get_name_servers():
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))
    name_servers = []
    with open("{}/{}".format(basedir, "/Config/resolv.conf"), "r") as rconfig:
        lines = rconfig.readlines()
        for line in lines:
            ip = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line)
            if ip:
                name_servers.append(ip.group(0))

    return name_servers


def health_check_dns_server(name_servers):
    _, domain_name, RDCLASS, _ = get_config_data()
    dns_domain = dns.name.from_text(domain_name)
    if not dns_domain.is_absolute():
        dns_domain = dns_domain.concatenate(dns.name.root)
    req = dns.message.make_query(dns_domain, dns.rdatatype.ANY)
    req.flags != dns.flags.AD
    req.find_rrset(req.additional, dns.name.root, RDCLASS, dns.rdatatype.OPT, create=True, force_unique=True)
    result_health_check_dns_server = []
    for name_server in name_servers:
        if check_DNS_port_open(domain_name, name_server):
            res = dns.query.udp(req, name_server)
            if res:
                result_health_check_dns_server.append({
                    "name_server": name_server,
                    "status": True
                })
        else:
            result_health_check_dns_server.append({
                "name_server": name_server,
                "status": False
            })
    return result_health_check_dns_server


