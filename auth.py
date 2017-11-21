#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
