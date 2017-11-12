#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pymongo
import json


_client = pymongo.MongoClient('localhost')
_db = _client.ples
_col = _db.questions

_COMMAND = 'command'
_ID = 'id'


def add(cid: str, command: str) -> bool:
    if exists(cid):
        return False
    _col.insert({_ID: cid, _COMMAND: command})
    return True


def exists(cid: str) -> bool:
    return _col.find({_ID: cid}).count() > 0


def get(cid: str) -> str:
    return _col.find_one({_ID: cid})


def command_line(cid: str, target: [str], output: str) -> str:
    command = get(cid)
    return command.replace('$^', ' '.join(target)).replace('$@', output)


def add_from_list(data_list: [dict]):
    for datum in data_list:
        add(datum['id'], datum['command'])


def add_from_json_file(filename: str):
    with open(filename, 'r', encoding='utf-8') as fp:
        add_from_list(json.load(fp))


if __name__ == '__main__':
    add_from_json_file(input('JSON file path >>> '))
