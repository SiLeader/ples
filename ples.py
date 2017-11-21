#!/usr/bin/env python3
"""
Programming Language Exercise System
"""

from flask import Flask, render_template, redirect, request, session
import util
from model import users
import auth

app = Flask(__name__)
app.config['SECRET_KEY'] = util.random_string()


@app.route('/')
def hello_world():
    return render_template('top.html')


@app.route('/user_top')
def user_top():
    return render_template('user_top.html')


@app.route('/question')
def question():
    return render_template('question.html', q={"sentence": "qqq", "test": "ppp", "result": "ooo", "language": "c_cpp"})


@app.route('/auth', methods=['POST'])
def authenticate():
    uid = request.form['id']
    pw = request.form['password']
    if users.check(uid, pw) and auth.login(uid):
        return redirect('/user_top')

    session['login-comment'] = 'サインインに失敗しました'
    return redirect('/auth')


if __name__ == '__main__':
    app.run()
