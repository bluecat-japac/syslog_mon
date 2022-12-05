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

import random
import socket
import struct


class SendDNSPkt:

    def __init__(self, url, server_ip, source_ip=None, port=53):
        self.url = url
        self.server_ip = server_ip
        if source_ip is None:
            source_ip = ''
        self.source_ip = source_ip
        self.port = port

    def sendPkt(self, packet, socket_module):
        sock = socket.socket(socket_module, socket.SOCK_DGRAM)
        sock.connect((self.source_ip, self.port)) if self.source_ip else sock.connect((self.server_ip, self.port))
        sock.settimeout(1)
        sock.sendall(bytes(packet))
        data = sock.recv(1024)
        sock.close()
        return data

    def _build_packet(self):
        randint = random.randint(0, 65535)
        packet = struct.pack(">H", randint)
        packet += struct.pack(">H", 0x0100)
        packet += struct.pack(">H", 1)
        packet += struct.pack(">H", 0)
        packet += struct.pack(">H", 0)
        packet += struct.pack(">H", 0)
        split_url = self.url.split(".")
        for part in split_url:
            packet += struct.pack("B", len(part))
            for s in part:
                packet += struct.pack('c',s.encode())
        packet += struct.pack("B", 0)
        packet += struct.pack(">H", 1)
        packet += struct.pack(">H", 1)
        return packet


def check_DNS_port_open(domain, nameserver, sourceip):
    s = SendDNSPkt(domain, nameserver, sourceip)
    portOpen = False
    for _ in range(5): # udp is unreliable.Packet loss may occur
        try:
            pkt = s._build_packet()
            data = s.sendPkt(pkt, socket.AF_INET) if '.' in nameserver else s.sendPkt(pkt, socket.AF_INET6)
            portOpen = True
            return portOpen
        except socket.timeout:
            pass
    return portOpen
