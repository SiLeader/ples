#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright 2017 SiLeader.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import string
import random
import hashlib
import base64
import re
import datetime


def random_string(length=64):
    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(length)])


_HASH_STRETCH_COUNT = 10000


def _to_salted(src):
    _HASH_SALT_COUNT = 16
    bases = [
        base64.b16encode(src.encode('utf-8')).decode('utf-8'),
        base64.b32encode(src.encode('utf-8')).decode('utf-8'),
        base64.b64encode(src.encode('utf-8')).decode('utf-8'),
        base64.b85encode(src.encode('utf-8')).decode('utf-8')
    ]
    salted = []
    for i in range(_HASH_SALT_COUNT):
        salted.append(bases[i % len(bases)])
        salted.append(src)
    return ''.join(salted)


def compute_hash(src):
    _VERSION = 0
    for i in range(_HASH_STRETCH_COUNT):
        src = hashlib.sha512(_to_salted(src).encode('utf-8')).hexdigest()
    return '$' + str(_VERSION) + '$' + src


def get_hash_version(hash_str):
    r = re.compile('^\$(\d)\$')
    m = r.match(hash_str)
    if not m:
        return None
    return int(m.group(1))


def get_current_datetime():
    return datetime.datetime.now(tz=datetime.timezone.utc)


def get_datetime_with_timezone(time_string, format_string, tz):
    dt = datetime.datetime.strptime(time_string, format_string)
    dt_tz = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond,
                              tz)
    return dt_tz


if __name__ == '__main__':
    target = input('>>> ')
    print(compute_hash(target))