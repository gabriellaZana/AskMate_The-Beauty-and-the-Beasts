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
            create_list[2] = line[2]
            table[int(request.form["id"])-1] = create_list
            counter = False
    if counter:
        table.append(create_list)
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
    return render_template('question.html', q_list=q_list, a_list=a_list, id_pos=id_pos)


@app.route('/save-Answer', methods=['POST'])
def route_save_answer():
    label_list = ["id", "Answer"]
    formdata = request.form
    create_list = []
    create_list.extend((common.id_generator("data/answer.csv"), time.time(), "0"))
    for label in label_list:
        for key, value in formdata.items():
            if label == key:
                create_list.append(value)
    create_list.append("image")
    print(create_list)
    common.append_story(create_list, "data/answer.csv")
    return redirect('/question/'+ request.form["id"])


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
    for line in q_list:
        if id_pos == int(line[0]):
            q_list[id_pos-1].append("deleted")
    common.export_story("data/question.csv", q_list)
    return redirect('/')


@app.route('/delete-answer/<questionid>/<answerid>/')
def route_delete_answer(questionid=None, answerid=None):
    id_pos = int(answerid)
    q_list = common.import_story("data/answer.csv")
    for line in q_list:
        if id_pos == int(line[0]):
            q_list[id_pos-1].append("deleted")
    common.export_story("data/answer.csv", q_list)
    return redirect('/question/'+questionid+'/')


@app.route('/question/<questionid>/<answerid>/vote-up/')
def route_upvote_answer(questionid=None, answerid=None):
    id_pos = int(answerid)
    id_question = questionid
    q_list = common.import_story("data/answer.csv")
    for line in q_list:
        if id_pos == int(line[0]):
            q_list[id_pos-1][2] = int(q_list[id_pos-1][2])
            q_list[id_pos-1][2] += 1
    common.export_story("data/answer.csv", q_list)
    return redirect('/question/' + id_question + "/")


@app.route('/question/<questionid>/<answerid>/vote-down/')
def route_downvote_answer(questionid=None, answerid=None):
    id_pos = int(answerid)
    id_question = questionid
    q_list = common.import_story("data/answer.csv")
    for line in q_list:
        if id_pos == int(line[0]):
            q_list[id_pos-1][2] = int(q_list[id_pos-1][2])
            q_list[id_pos-1][2] += -1
    common.export_story("data/answer.csv", q_list)
    return redirect('/question/' + id_question + "/")


@app.route('/question/<questionid>/vote-up')
def route_upvote_question(questionid=None):
    id_pos = int(questionid)
    q_list = common.import_story("data/question.csv")
    for line in q_list:
        if id_pos == int(line[0]):
            q_list[id_pos-1][3] = int(q_list[id_pos-1][3])
            q_list[id_pos-1][3] += 1
    common.export_story("data/question.csv", q_list)
    return redirect('/')

@app.route('/question/<questionid>/vote-down')
def route_downvote_question(questionid=None):
    id_pos = int(questionid)
    q_list = common.import_story("data/question.csv")
    for line in q_list:
        if id_pos == int(line[0]):
            q_list[id_pos-1][3] = int(q_list[id_pos-1][3])
            q_list[id_pos-1][3] += -1
    common.export_story("data/question.csv", q_list)
    return redirect('/')


@app.route('/question/<questionid>/new-answer')
def new_answer(questionid):
    return render_template('form.html', form="Answer", data=[questionid,"","","","",""])


@app.route("/viewcount/<questionid>", methods=["POST"])
def viewcount(questionid):
    table = common.import_story("data/question.csv")
    for record in table:
        if record[0] == questionid:
            record[2] = int(record[2])
            record[2] += 1
    common.export_story("data/question.csv", table)
    return redirect('/question/' + questionid + "/")



if __name__ == "__main__":
    app.secret_key = "whoeventriestoguessthis"
    app.run(
        debug=True,
        port=5000
    )
