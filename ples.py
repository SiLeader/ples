#!/usr/bin/env python3
"""
Programming Language Exercise System
"""

from flask import Flask, render_template, redirect, request, session
import util
from model import users
from model import questions
import auth

app = Flask(__name__)
app.config['SECRET_KEY'] = util.random_string()


@app.route('/')
def hello_world():
    return render_template('top.html')


@app.route('/user_top')
def user_top():
    qs = questions.get_list()
    return render_template('user_top.html', require_questions=qs)


@app.route('/question', methods=['POST', 'GET'])
def question():
    if request.method == 'POST':
        return redirect('/question?id=' + request.form["question_id"])
    else:
        q = request.args.get("id", default=None, type=str)
        if q is None:
            return redirect('/user_top')
        q = questions.get(q)
        return render_template('question.html', q=q)


@app.route('/submit/json', methods=["POST"])
def submit_json():
    data = request.form["data"]
    qid = request.form["id"]
    if questions.check_to_create_temporary_file(qid, data):
        return {"result": True}
    return {"result": False}


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
