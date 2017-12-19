#!/usr/bin/env python
# -*- coding:utf-8 -*-

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

import pymongo
import util
import json


_client = pymongo.MongoClient('localhost')
_db = _client.ples
_col = _db.users

_USER_ID = 'id'
_PASSWORD = 'password'
_NAME = 'name'
_QUESTION_RESULTS = 'results'

"""
users
|
|-id str
|-password str
|-name str
|-results {}
  |-{qid} []
    |-passed bool
"""


def add(uid: str, pw: str, name: str) -> bool:
    """
    Add user to database
    :param uid: User ID (Unique)
    :param pw: Password (Hashed and non-hashed)
    :param name: User display name
    :return: added status. True -> Success, False -> Failed
    """
    if exists(uid):
        return False
    if util.get_hash_version(pw) is None:
        pw = util.compute_hash(pw)
    _col.insert({_USER_ID: uid, _PASSWORD: pw, _NAME: name, _QUESTION_RESULTS: {}})
    return True


def exists(uid: str) -> bool:
    """
    Check exists in user Database
    :param uid: Target user id
    :return: True -> already exist, False -> not exist
    """
    return _col.find({_USER_ID: uid}).count() > 0


def remove(uid: str):
    """
    Remove user from database
    :param uid: Target user id
    """
    _col.remove({_USER_ID: uid})


def update(uid: str, pw: str=None, name: str=None) -> bool:
    """
    Update user information
    :param uid: Target user ID
    :param pw: Password (None is ignored)
    :param name: Display name (None is ignored)
    :return: True -> Success, False -> Failed
    """
    if pw is None and name is None:
        return False
    if not exists(uid):
        return False

    data = {}
    if pw is not None:
        if util.get_hash_version(pw) is None:
            pw = util.compute_hash(pw)
        data[_PASSWORD] = pw
    if name is not None:
        data[_NAME] = name

    _col.update({_USER_ID: uid}, {'$set': data}, multi=False)
    return True


def check(uid: str, pw: str) -> bool:
    if not exists(uid):
        return False

    if util.get_hash_version(pw) is None:
        pw = util.compute_hash(pw)

    user = _col.find_one({_USER_ID: uid})
    return user[_PASSWORD] == pw


def update_result(uid: str, qid: str, results: bool):
    user = _col.find_one({_USER_ID: uid})
    res = user[_QUESTION_RESULTS]

    res[qid] = results
    _col.update({_USER_ID: uid}, {'$set': {_QUESTION_RESULTS: res}})


def get_result(uid: str, qid: str):
    user = _col.find_one({_USER_ID: uid})
    res = user[_QUESTION_RESULTS]
    return qid in res and res[qid]


def remove_cleared(uid: str, question: [dict]):
    res = []
    for q in question:
        if not get_result(uid, q["id"]):
            res.append(q)
    return res


if __name__ == '__main__':
    json_file = input('JSON file path >>> ')

    with open(json_file, encoding='utf-8') as json_:
        json_data = json.load(json_)
        for json in json_data:
            add(json['id'], json["password"], json["name"])
