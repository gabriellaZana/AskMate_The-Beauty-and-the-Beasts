from flask import Flask, render_template, redirect, request, session, url_for
import common
import time
from datetime import datetime
question_keys = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
answer_keys = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


app = Flask(__name__)


@app.route('/save-Question', methods=['POST'])
def route_save_question():
    if int(request.form["question_id"]) > -1:
        common.query_handler("UPDATE question SET title=%s, message=%s, image=%s WHERE id=%s", (request.form["title"],request.form["Question"],request.form["image"], request.form["question_id"]))
    else:
        common.query_handler("INSERT INTO question (submission_time, view_number, vote_number, title, message, image) VALUES(%s,%s,%s,%s,%s,%s)", (datetime.now(),0,0,request.form["title"],request.form["Question"],request.form["image"]))
    return redirect('/list')


@app.route('/new-question')
def route_new_question():
    title_help = True
    return render_template('form_new_question.html', title_help=title_help, form="Question")


@app.route("/")
@app.route("/list")
def index():
    database = common.query_handler("SELECT * FROM question")
    return render_template("list.html", database=database)


@app.route('/question/<questionid>/')
def route_question_page(questionid=None):
    id_num = questionid
    question_database = common.query_handler("SELECT * FROM question WHERE id=%s",(id_num,))
    answer_database = common.query_handler("SELECT * FROM answer WHERE question_id=%s", (id_num,))
    return render_template('question.html', question_database=question_database, answer_database=answer_database, id_num=id_num)


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
    edit = True
    id_num = questionid
    database = common.query_handler("SELECT * FROM question WHERE id=%s;", (id_num,))
    return render_template('form.html', edit=edit, id_num=id_num, database=database, form="Question")


@app.route('/delete-question/<questionid>/')
def route_delete_question(questionid=None):
    id_num = questionid
    common.query_handler("DELETE FROM question WHERE id=%s",(id_num,))
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
    id_num = questionid
    common.query_handler("UPDATE question SET vote_number = vote_number+1 WHERE id=%s",(id_num,))
    return redirect('/')


@app.route('/question/<questionid>/vote-down')
def route_downvote_question(questionid=None):
    id_num = questionid
    common.query_handler("UPDATE question SET vote_number = vote_number-1 WHERE id=%s",(id_num,))
    return redirect('/')


@app.route('/question/<questionid>/new-answer')
def new_answer(questionid):
    id_num = questionid
    add_answer = False
    question_list = common.import_story("data/question.csv")
    return render_template('form.html', form="Answer", add_answer=add_answer, id_num=id_num, question_list=question_list, data=[questionid,"","","","","",""])


@app.route("/viewcount/<questionid>", methods=["POST"])
def viewcount(questionid):
    table = common.query_handler("UPDATE question SET view_number = view_number + 1 WHERE id=%s", (questionid,))
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
