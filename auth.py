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

import datetime

from flask import session

import util
from model import users

_LIMIT = datetime.timedelta(hours=5)
_STR_FORMAT = '%Y-%m-%d %H:%M:%S'


def login(uid):
    session['id'] = uid
    session['limit'] = (util.get_current_datetime() + _LIMIT).strftime(_STR_FORMAT)
    return True


def check():
    if session.get('id') is None or session.get('limit') is None:
        logout()
        return False
    if not session['id'].endswith('@teec.in.net') and not users.exists(session['id']):
        logout()
        return False

    dt = util.get_datetime_with_timezone(session['limit'], _STR_FORMAT, datetime.timezone.utc)
    current = util.get_current_datetime()

    if dt <= current:
        logout()
        return False

    return login(session['id'])


def logout():
    if session.get('id') is not None:
        session.pop('id')
    if session.get('limit') is not None:
        session.pop('limit')
    return True


def get_id():
    if check():
        return session['id']
    return None
