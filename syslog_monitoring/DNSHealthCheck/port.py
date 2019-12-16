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

    def __init__(self,url,serverIP,port=53):
        self.url=url
        self.serverIP = serverIP
        self.port=port

    def sendPkt(self, packet):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)
        sock.sendto(bytes(packet), (self.serverIP, self.port))
        data, addr = sock.recvfrom(1024)
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


def check_DNS_port_open(domain, nameserver):
    s = SendDNSPkt(domain, nameserver)
    portOpen = False
    for _ in range(5): # udp is unreliable.Packet loss may occur
        try:
            pkt = s._build_packet()
            s.sendPkt(pkt)
            portOpen = True
            return portOpen
        except socket.timeout:
            pass
    return portOpen
