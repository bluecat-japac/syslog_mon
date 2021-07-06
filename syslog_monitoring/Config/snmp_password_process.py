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

import base64


def encrypt_password(password):
    return base64.b64encode(password)


def decrypt_password(encoded):
    return base64.b64decode(encoded)


if __name__ == '__main__':
    while True:
        password = raw_input("Let's type a new password:")
        if password.strip() is not "":
            break
    pwd_encrypt = encrypt_password(password.strip())
    print "{0} {1}".format("Your password is encrypted as:", pwd_encrypt)
    print "Please update your encrypted password in snmp_config.json file\n"
