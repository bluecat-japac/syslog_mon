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


def get_engine_id():
    basedir = os.path.dirname(__file__)
    config_file = os.path.join(basedir, "snmpd.conf")
    for i, line in enumerate(open(config_file)):
        pattern = re.compile(r"\boldEngineID.[a-zA-Z0-9]+\b")
        if line is None:
            continue
        else:
            match = re.search(pattern, line)
            if match is not None:
                engine_id = match.group().split(" 0x")[1]
                return engine_id
