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


REG_TARGET_STRING_IP = r"(client|master|from).\d+\.\d+\.\d+\.\d+"
REG_TARGET_IP = r"\d+\.\d+\.\d+\.\d+"
REG_ZONE_STRING = r"(zone|transfer of ').(\w+[\.-]?)+/IN/(\w+[\.-]?)+"
REG_ZONE = r"(\w+[\.-]?)+/IN/(\w+[\.-]?)+"
REG_INTERFACE_STRING_DOWN = r"Deleting interface .+ \w+\.*\w+,"
REG_INTERFACE_STRING_UP = r"Listen normally on \d+ \w+\.*\w+"
REG_INTERFACE = r"\w+\.*\w+,"
