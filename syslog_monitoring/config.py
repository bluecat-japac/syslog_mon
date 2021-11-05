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
from logging.handlers import RotatingFileHandler
import os
import sys
import configparser
import gzip

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


class NewRotatingFileHandler(RotatingFileHandler):
    def __init__(self, filename, **kws):
        backupCount = kws.get('backupCount', 0)
        self.backup_count = backupCount
        RotatingFileHandler.__init__(self, filename, **kws)

    def doArchive(self, old_log):
        with open(old_log) as log:
            with gzip.open(old_log + '.gz', 'wb') as comp_log:
                comp_log.writelines(log)
        os.remove(old_log)

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        if self.backup_count > 0:
            for i in range(self.backup_count - 1, 0, -1):
                sfn = "%s.%d.gz" % (self.baseFilename, i)
                dfn = "%s.%d.gz" % (self.baseFilename, i + 1)
                if os.path.exists(sfn):
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)
            dfn = self.baseFilename + ".1"
            if os.path.exists(dfn):
                os.remove(dfn)
            if os.path.exists(self.baseFilename):
                os.rename(self.baseFilename, dfn)
                self.doArchive(dfn)
        if not self.delay:
            self.stream = self._open()


def map_text_log_level(logging_text):
    """
    :param logging_text: content of log
    :return:
    [dict_log] - String
    """
    dict_log = dict(
        CRITICAL=50,
        FATAL=50,
        ERROR=40,
        WARNING=30,
        WARN=30,
        INFO=20,
        DEBUG=10,
        NOTSET=0
    )
    return dict_log[logging_text]


# Configure log app monitoring
default_maxbytes = 10000000
default_backupcount = 5
default_log_level = "WARNING"
basedir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(basedir, "Config", "config.ini")
config = configparser.ConfigParser()
config.read(config_file)
maxbytes = config.getint("LOGGER_CONFIG", "MAXBYTES") if config is not None and config.has_option("LOGGER_CONFIG", "MAXBYTES") else default_maxbytes
backupcount = config.getint("LOGGER_CONFIG", "BACKUPCOUNT") if config is not None and config.has_option("LOGGER_CONFIG", "BACKUPCOUNT") else default_backupcount
log_level = config.get("LOGGER_CONFIG", "LOG_LEVEL") if config is not None and config.has_option("LOGGER_CONFIG", "LOG_LEVEL") else default_log_level
log_level = map_text_log_level(log_level)

logger = logging.getLogger("monitoring")
logger.setLevel(level=log_level)
handler = NewRotatingFileHandler(LOG_PATH + "/" + LOG_NAME, maxBytes=maxbytes, backupCount=backupcount)
log_formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
handler.setFormatter(log_formatter)
logger.addHandler(handler)
