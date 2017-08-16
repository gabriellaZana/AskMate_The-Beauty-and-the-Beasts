from flask import Flask, render_template, redirect, request, session, url_for
import common
import time
from datetime import datetime

app = Flask(__name__)


@app.route('/save-Question', methods=['POST'])
def route_save_question():
    label_list = ["title", "Question"]
    formdata = request.form
    table = common.import_story("data/question.csv")
    print(table)
    create_list = []
    create_list.extend(((common.id_generator("data/question.csv")), time.time(), "0", "0"))
    for label in label_list:
        for key, value in formdata.items():
            if label == key:
                create_list.append(value)
    create_list.append("image")
    print(create_list)
    table.append(create_list)
    common.export_story("data/question.csv", table)
    return redirect('/list')


@app.route('/new-question')
def route_new_question():
    return render_template('form.html', form="Question")


@app.route("/")
@app.route("/list")
def index():
    database = common.import_story("data/question.csv")
    return render_template("list.html", database=database)


@app.route('/question/<questionid>/')
def route_question_page(questionid=None):
    id_pos = questionid
    q_list = common.import_story("data/question.csv")
    a_list = common.import_story("data/answer.csv")
    return render_template('question.html', q_list=q_list, a_list=a_list, id_pos=id_pos)


@app.route('/save-answer', methods=['POST'])
def route_save_answer(questionid):
    data = []
    data.append(get_last_row("data/anwser.csv"))
    data.append(time.time())
    data.append("0")
    data.append(questionid)
    data.append(request.form[Answer])
    data.append("image")
    table = common.import_story("data/answer.csv")
    table.append(data)
    common.export_story("data/answer.csv", table)
    return render_template('/question/<questionid>')


@app.route('/edit-question/<questionid>', methods=['POST'])
def route_edit_question(questionid=None):
    pass #return redirect('/')


@app.route('/delete-question/<questionid>/')
def route_delete_question(questionid=None):
    id_pos = int(questionid)
    q_list = common.import_story("data/question.csv")
    for line in q_list:
        if id_pos == int(line[0]):
            q_list[id_pos-1].append("deleted")
    common.export_story("data/question.csv", q_list)
    return redirect('/')


@app.route('/question/<questionid>/new-answer')
def new_answer(questionid):
    return render_template('form.html', form="Answer")


if __name__ == "__main__":
    app.secret_key = "whoeventriestoguessthis"
    app.run(
        debug=True,
        port=5000
    )
