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
import json
import uuid
from model import execute

_client = pymongo.MongoClient('localhost')
_db = _client.ples
_col = _db.questions


_ID = 'id'
_LANGUAGE = 'language'
_CATEGORY = 'category'
_TITLE = 'title'
_SENTENCE = 'sentence'
_TEST_DATA = 'test'
_EXEC_SYSTEM = 'exec'


def add(qid: str, _title: str, category: str,
        lang: str, sentence: str, test_data: [str], exec_system: str):
    """
    add questions
    :param qid: question id (unique)
    :param _title: question title
    :param category: question category
    :param lang: programming language
    :param sentence: problem sentence
    :param test_data: validation check test data
    :param exec_system: execution command id (see execute.py)
    :return: status
    """
    _col.insert({
        _ID: qid,
        _TITLE: _title,
        _CATEGORY: category,
        _LANGUAGE: lang,
        _SENTENCE: sentence,
        _TEST_DATA: test_data,
        _EXEC_SYSTEM: exec_system
    })
    return True


def exists(qid: str):
    """
    check exist item from qid or title
    :param qid: question id
    :return: is exist
    """
    return _col.find({_ID: qid}).count() > 0


def get(qid):
    if not exists(qid):
        return {}
    return _col.find_one({_ID: qid})


def get_list():
    return list(_col.find())


def check_to_create_temporary_file(qid: str, data: [str]) -> bool:
    q = get(qid)
    cid = q[_EXEC_SYSTEM]
    output = "/tmp/" + uuid.uuid4().hex
    for test in q[_TEST_DATA]:
        result = execute.run_to_create_temporary_file(cid, data, output, test["args"], test["stdin"])
        stdout = result.stdout.decode('utf-8')
        if result is None or result.returncode != 0:
            return False
        if stdout != test["result"]["stdout"]:
            return False
    return True


def remove(qid: str):
    """
    Remove user from database
    :param qid: Target question id
    """
    _col.remove({_ID: qid})


if __name__ == '__main__':
    json_file = input('JSON file path >>> ')

    with open(json_file, encoding='utf-8') as json_:
        json_data = json.load(json_)
        for json in json_data:
            add(
                json['id'],
                json['title'],
                json['category'],
                json['language'],
                json['sentence'],
                json['tests'],
                json['exec']
            )
