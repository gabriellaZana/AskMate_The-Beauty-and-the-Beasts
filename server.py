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
    comment_database = common.query_handler("SELECT * FROM comment WHERE question_id=%s", (id_num,))
    return render_template('question.html', question_database=question_database, answer_database=answer_database, id_num=id_num, comment_database=comment_database)


@app.route('/save-Answer', methods=['POST'])
def route_save_answer():
    formdata = request.form
    common.query_handler("""INSERT INTO answer (submission_time, vote_number, question_id, message, image)
                            VALUES(%s, %s, %s, %s, %s)""",(datetime.now(), 0, formdata['question_id'], formdata['Answer'], formdata['image']))
    return redirect('/question/' + request.form['question_id'])


@app.route('/save-Comment', methods=['POST'])
def route_save_comment():
    formdata = request.form
    common.query_handler("""INSERT INTO comment (question_id, message, submission_time, edited_count)
                            VALUES(%s, %s, %s, %s)""",(formdata['question_id'], formdata['Comment'], datetime.now(), 0))
    return redirect('/question/' + request.form['question_id'])


@app.route('/update-Comment', methods=['POST'])
def route_update_comment():
    formdata = request.form
    common.query_handler("""UPDATE comment SET message=%s, edited_count = edited_count + 1
                            WHERE id=%s""",(formdata['Comment'], formdata['comment_id']))
    return redirect('/question/' + request.form['question_id'])


@app.route('/edit-question/<questionid>/')
def route_edit_question(questionid=None):
    edit = True
    id_num = questionid
    database = common.query_handler("SELECT * FROM question WHERE id=%s;", (id_num,))
    return render_template('form_edit_question.html', edit=edit, id_num=id_num, database=database, form="Question")


@app.route('/delete-question/<questionid>/')
def route_delete_question(questionid=None):
    id_num = questionid
    common.query_handler("DELETE FROM question WHERE id=%s",(id_num,))
    return redirect('/')


@app.route('/delete-answer/<questionid>/<answerid>/')
def route_delete_answer(questionid=None, answerid=None):
    id_num = int(answerid)
    common.query_handler("DELETE FROM answer WHERE id=%s",(id_num,))
    return redirect('/question/'+questionid+'/')


@app.route('/comments/<comment_id>/edit')
def edit_comment(comment_id):
    question_database = common.query_handler("SELECT * FROM question INNER JOIN comment ON question.id=comment.question_id WHERE comment.id=%s",(comment_id,))
    comment_database = common.query_handler("SELECT * FROM comment WHERE id=%s",(comment_id,))
    return render_template("form_edit_comment.html", form="Comment", comment_database=comment_database, question_database=question_database)


@app.route('/comments/<comment_id>/delete')
def delete_comment(comment_id):
    questionid = common.query_handler("SELECT question_id FROM comment WHERE id=%s",(int(comment_id),))
    common.query_handler("DELETE FROM comment WHERE id=%s",(comment_id,))
    return redirect('/question/'+str(questionid[0]["question_id"])+'/')



@app.route('/question/<questionid>/<answerid>/vote-up/')
def route_upvote_answer(questionid=None, answerid=None):
    id_num = int(answerid)
    id_question = questionid
    common.query_handler("UPDATE answer SET vote_number = vote_number+1 WHERE id=%s",(id_num,))
    return redirect('/question/' + id_question + "/")


@app.route('/question/<questionid>/<answerid>/vote-down/')
def route_downvote_answer(questionid=None, answerid=None):
    id_num = answerid
    id_question = questionid
    common.query_handler("UPDATE answer SET vote_number = vote_number-1 WHERE id=%s",(id_num,))
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
    add_answer = True
    question_database = common.query_handler("SELECT * FROM question WHERE id=%s", (id_num,))
    return render_template('form_new_answer.html', form="Answer", add_answer=add_answer, id_num=id_num, question_database=question_database)


@app.route('/question/<questionid>/new-comment')
def new_comment(questionid):
    id_num = questionid
    add_answer = True
    question_database = common.query_handler("SELECT * FROM question WHERE id=%s", (id_num,))
    return render_template('form_new_answer.html', form="Comment", add_answer=add_answer, id_num=id_num, question_database=question_database)


@app.route("/viewcount/<questionid>", methods=["POST"])
def viewcount(questionid):
    table = common.query_handler("UPDATE question SET view_number = view_number + 1 WHERE id=%s", (questionid,))
    return redirect('/question/' + questionid + "/")


if __name__ == "__main__":
    app.secret_key = "whoeventriestoguessthis"
    app.run(
        debug=True,
        port=5000
    )
