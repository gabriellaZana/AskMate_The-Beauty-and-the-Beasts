from flask import Flask, render_template, redirect, request, session, url_for
import common
import time
from datetime import datetime


app = Flask(__name__)


@app.route('/save-Question', methods=['POST'])
def route_save_question():
    label_list = ["title", "Question", "image"]
    formdata = request.form
    table = common.import_story("data/question.csv")
    create_list = []
    create_list.extend(((common.id_generator("data/question.csv")), time.time(), "0", "0"))
    for label in label_list:
        for key, value in formdata.items():
            if label == key:
                create_list.append(value)
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
    title_help = True
    return render_template('form.html', title_help=title_help, form="Question", data=["0","","","","","",""])


@app.route("/")
@app.route("/list")
def index():
    database = common.import_story("data/question.csv")
    timestamp_list = []
    for row in database:
        timestamp_list.append(datetime.fromtimestamp(int(float(row[1]))))
    return render_template("list.html", database=database, timestamp_list=timestamp_list)


@app.route('/question/<questionid>/')
def route_question_page(questionid=None):
    id_num = questionid
    question_list = common.import_story("data/question.csv")
    answer_list = common.import_story("data/answer.csv")
    timestamp_list = []
    for row in answer_list:
        timestamp_list.append(datetime.fromtimestamp(int(float(row[1]))))
    return render_template('question.html', question_list=question_list, answer_list=answer_list, id_num=id_num, timestamp_list=timestamp_list)


@app.route('/save-Answer', methods=['POST'])
def route_save_answer():
    label_list = ["id", "Answer", "image"]
    formdata = request.form
    create_list = []
    create_list.extend((common.id_generator("data/answer.csv"), time.time(), "0"))
    for label in label_list:
        for key, value in formdata.items():
            if label == key:
                create_list.append(value)
    common.append_story(create_list, "data/answer.csv")
    return redirect('/question/' + request.form["id"])


@app.route('/edit-question/<questionid>/')
def route_edit_question(questionid=None):
    id_num = int(questionid)
    table = common.import_story("data/question.csv")
    data = []
    for line in table:
        if line[0] == str(id_num):
            data = line
    return render_template('form.html', data=data, table=table, form="Question")


@app.route('/delete-question/<questionid>/')
def route_delete_question(questionid=None):
    id_num = int(questionid)
    question_list = common.import_story("data/question.csv")
    for line in question_list:
        if id_num == int(line[0]):
            line.append("deleted")
    common.export_story("data/question.csv", question_list)
    return redirect('/')


@app.route('/delete-answer/<questionid>/<answerid>/')
def route_delete_answer(questionid=None, answerid=None):
    id_num = int(answerid)
    question_list = common.import_story("data/answer.csv")
    for line in question_list:
        if id_num == int(line[0]):
            line.append("deleted")
    common.export_story("data/answer.csv", question_list)
    return redirect('/question/'+questionid+'/')


@app.route('/question/<questionid>/<answerid>/vote-up/')
def route_upvote_answer(questionid=None, answerid=None):
    id_num = int(answerid)
    id_question = questionid
    question_list = common.import_story("data/answer.csv")
    for line in question_list:
        if id_num == int(line[0]):
            line[2] = int(line[2])
            line[2] += 1
    common.export_story("data/answer.csv", question_list)
    return redirect('/question/' + id_question + "/")


@app.route('/question/<questionid>/<answerid>/vote-down/')
def route_downvote_answer(questionid=None, answerid=None):
    id_num = int(answerid)
    id_question = questionid
    question_list = common.import_story("data/answer.csv")
    for line in question_list:
        if id_num == int(line[0]):
            line[2] = int(line[2])
            line[2] += -1
    common.export_story("data/answer.csv", question_list)
    return redirect('/question/' + id_question + "/")


@app.route('/question/<questionid>/vote-up')
def route_upvote_question(questionid=None):
    id_num = int(questionid)
    question_list = common.import_story("data/question.csv")
    for line in question_list:
        if id_num == int(line[0]):
            line[3] = int(line[3])
            line[3] += 1
    common.export_story("data/question.csv", question_list)
    return redirect('/')


@app.route('/question/<questionid>/vote-down')
def route_downvote_question(questionid=None):
    id_num = int(questionid)
    question_list = common.import_story("data/question.csv")
    for line in question_list:
        if id_num == int(line[0]):
            line[3] = int(line[3])
            line[3] += -1
    common.export_story("data/question.csv", question_list)
    return redirect('/')


@app.route('/question/<questionid>/new-answer')
def new_answer(questionid):
    id_num = questionid
    add_answer = False
    question_list = common.import_story("data/question.csv")
    return render_template('form.html', form="Answer", add_answer=add_answer, id_num=id_num, question_list=question_list, data=[questionid,"","","","","",""])


@app.route("/viewcount/<questionid>", methods=["POST"])
def viewcount(questionid):
    table = common.import_story("data/question.csv")
    for record in table:
        if record[0] == questionid:
            record[2] = int(record[2])
            record[2] += 1
    common.export_story("data/question.csv", table)
    return redirect('/question/' + questionid + "/")


@app.route("/sortbyViews")
def sortbyID():
    common.sortbynumber(2)
    return redirect("/")


@app.route("/sortbySubmission")
def sortbySubmission():
    common.sortbynumber(1)
    return redirect("/")


@app.route("/sortbyVotes")
def sortbyVotes():
    common.sortbynumber(3)
    return redirect("/")

if __name__ == "__main__":
    app.secret_key = "whoeventriestoguessthis"
    app.run(
        debug=True,
        port=5000
    )
