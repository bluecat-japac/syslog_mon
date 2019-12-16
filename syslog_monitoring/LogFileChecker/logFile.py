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

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from config import logger, LOG_DATE_LIMITED
from path import Path
import time


def deleteFile(file):
    file.remove()
    logger.info("Delete file {}".format(file))


def cleanUpLog(path):
    try:
        items = Path(path)
        timeNow = time.time()
        for item in items.walk():
            if item.isfile() and os.path.getctime(item) < (timeNow - 86400*LOG_DATE_LIMITED):
                deleteFile(item)
    except FileNotFoundError or FileExistsError as ex:
        logger.error("Check log file: {}".format(ex))
