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

import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys

###
# Log config
###
LOG_DATE_LIMITED = 2
LOG_PATH = "/var/log/mon-app"
LOG_NAME = "monitor.log"
LOG_PRIORITY = {
    'emerg':60,
    'crit':60,
    'alert':60,
    'err':50,
    'warning':40,
    'notice':30,
    'info':20,
    'debug':10
}

# Configure log app monitoring
logging.basicConfig(
    level=logging.INFO,
)
logger = logging.getLogger("monitoring")
handler = TimedRotatingFileHandler(LOG_PATH + "/" + LOG_NAME, when="midnight", interval=1)
handler.suffix = "%Y%m%d"
log_formater = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
handler.setFormatter(log_formater)
logger.addHandler(handler)
