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
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import datetime
from logFile import cleanUpLog
from config import LOG_PATH

scheduler = BackgroundScheduler()

scheduler.add_job(cleanUpLog, 'cron', args=[LOG_PATH], hour=0)

scheduler.start()
atexit.register(lambda: scheduler.shutdown())
