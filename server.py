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
    create_list = []
    create_list.extend(((common.id_generator("data/question.csv")), time.time(), "0", "0"))
    for label in label_list:
        for key, value in formdata.items():
            if label == key:
                create_list.append(value)
    create_list.append("image")
    counter = True
    for line in table:
        if int(line[0]) == int(request.form["id"]):
            create_list[0] = request.form["id"]
            table[int(request.form["id"])-1] = create_list
            counter = False
    if counter:
        table.append(create_list)
    print(create_list)
    print(table)
    common.export_story("data/question.csv", table)
    return redirect('/list')


@app.route('/new-question')
def route_new_question():
    return render_template('form.html', form="Question", data=["0","","","","",""])


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
    viewcount(questionid, "data/question.csv")
    print(id_pos)
    print(q_list)
    return render_template('question.html', q_list=q_list, a_list=a_list, id_pos=id_pos)


@app.route('/save-answer', methods=['POST'])
def route_save_answer(questionid):
    formdata = request.form
    table = common.import_story("data/answer.csv")
    create_list = []
    create_list.extend((common.id_generator("data/answer.csv"), time.time(), "0", "0"))
    for key, value in formdata.items():
        if key == "Answer":
            create_list.append(value)
    create_list.append("image")
    table.append(create_list)
    common.export_story("data/answer.csv", table)
    return redirect('/question/<questionid>')


@app.route('/edit-question/<questionid>/')
def route_edit_question(questionid=None):
    id_pos = int(questionid)
    table = common.import_story("data/question.csv")
    data = []
    for line in table:
        if line[0] == str(id_pos):
            data = line
    return render_template('form.html', data=data, form="Question")


@app.route('/delete-question/<questionid>/')
def route_delete_question(questionid=None):
    id_pos = int(questionid)
    q_list = common.import_story("data/question.csv")
    print(q_list)
    print("valami")
    for line in q_list:
        if id_pos == int(line[0]):
            q_list[id_pos-1].append("deleted")
    common.export_story("data/question.csv", q_list)
    return redirect('/')


@app.route('/question/<questionid>/new-answer')
def new_answer(questionid):
    return render_template('form.html', form="Answer")


def viewcount(questionid, filename):
    table = common.import_story(filename)
    table[int(questionid)-1][2] = int(table[int(questionid)-1][2])
    table[int(questionid)-1][2] += 1
    common.export_story(filename, table)
    return



if __name__ == "__main__":
    app.secret_key = "whoeventriestoguessthis"
    app.run(
        debug=True,
        port=5000
    )
