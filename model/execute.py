#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pymongo
import json
import subprocess
import uuid
import os


_client = pymongo.MongoClient('localhost')
_db = _client.ples
_col = _db.executes

_COMMAND = 'command'
_ID = 'id'


def add(cid: str, command: str) -> bool:
    if exists(cid):
        return False
    _col.insert({_ID: cid, _COMMAND: command})
    return True


def exists(cid: str) -> bool:
    return _col.find({_ID: cid}).count() > 0


def get(cid: str) -> map:
    return _col.find_one({_ID: cid})


def command_line(cid: str, target: [str], output: str, args: [[str]]) -> [str]:
    commands = get(cid)[_COMMAND]
    cmds = []
    for i in range(min(len(args), len(commands))):
        cmds.append(commands[i].replace('$^', ' '.join(target)).replace('$@', output).replace('$#', ' '.join(args[i])))
    return cmds


def run(cid: str, target: [str], output: str, args: [[str]], stdin: [str]):
    cmd = command_line(cid, target, output, args)

    result = None
    for i in range(min(len(cmd), len(stdin))):
        result = subprocess.run(cmd[i].split(" "), input=stdin[i])
        if result.returncode != 0:
            break
    return result


def run_to_create_temporary_file(cid: str, target_code: [str], output: str, args: [[str]], stdin: [str]):
    files = []
    for t in target_code:
        file_name = "/tmp/" + uuid.uuid4().hex
        with open(file_name, "w") as file:
            file.write(t)
        files.append(file_name)
    if len(files) < len(target_code):
        return None
    result = run(cid, files, output, args, stdin)

    for file in files:
        os.remove(file)
    return result


def add_from_list(data_list: [dict]):
    for datum in data_list:
        add(datum['id'], datum['command'])


def add_from_json_file(filename: str):
    with open(filename, 'r', encoding='utf-8') as fp:
        add_from_list(json.load(fp))


if __name__ == '__main__':
    add_from_json_file(input('JSON file path >>> '))
