#!/usr/bin/env python3
"""
Programming Language Exercise System
"""

from flask import Flask, render_template, redirect, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('')


@app.route('/auth', methods=['POST'])
def authenticate():
    pass


if __name__ == '__main__':
    app.run()
