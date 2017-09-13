from flask import Flask, render_template, redirect, request, session, url_for
import common
import time
from datetime import datetime
question_keys = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
answer_keys = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


app = Flask(__name__)

# LIST


@app.route("/")
def latest_5():
    search = False
    database = common.query_handler("""SELECT question.id, question.submission_time, view_number, vote_number, title, message, image, users_id, user_name, reputation FROM question
                                     LEFT JOIN users ON users.id=users_id
                                     ORDER BY question.submission_time DESC LIMIT 5;""")
    return render_template("list.html", database=database, search=search)


@app.route("/list")
def index():
    sort = None
    search = False
    database = common.query_handler("""SELECT question.id, question.submission_time, view_number, vote_number, title, message, image, users_id, user_name, reputation FROM question
                                     LEFT JOIN users ON users.id=users_id;""")
    return render_template("list.html", database=database, search=search)


@app.route("/all-users")
def all_users():
    database = common.query_handler("SELECT * FROM users;")
    return render_template("user.html", database=database)


@app.route("/viewcount/<questionid>", methods=["POST"])
def viewcount(questionid):
    table = common.query_handler("UPDATE question SET view_number = view_number + 1 WHERE id=%s", (questionid,))
    return redirect('/question/' + questionid + "/")


@app.route("/search", methods=["POST"])
def search():
    search = True
    form_data = request.form
    question_database = common.query_handler("""SELECT DISTINCT question.id, answer.question_id
                                                FROM question FULL JOIN answer ON question.id = answer.question_id
                                                WHERE question.title ILIKE '%%' || %s || '%%'
                                                OR answer.message ILIKE '%%' || %s || '%%'
                                                OR question.message ILIKE '%%' || %s || '%%' ;""",
                                             (form_data['asksearch'], form_data['asksearch'], form_data['asksearch'],))
    database = common.query_handler("SELECT * FROM question")
    return render_template("list.html", phrase=form_data["asksearch"], question_database=question_database,
                           database=database, search=search)


@app.route('/tags')
def route_tags():
    database = common.query_handler("SELECT name, COUNT(question_id) AS question_number \
                                     FROM tag JOIN question_tag ON tag.id=question_tag.tag_id \
                                     GROUP BY name")
    return render_template("tags.html", database=database)


# REGISTRASION

@app.route('/registration')
def route_registration():
    return render_template("form_registration.html", isValid=True)


@app.route('/save-user', methods=["POST"])
def route_save_user():
    existing_users = common.query_handler("SELECT user_name FROM users")
    current_user = request.form["username"]
    for line in existing_users:
        if line["user_name"] == current_user:
            return render_template("form_registration.html", isValid=False)
    common.query_handler("INSERT INTO users (submission_time, user_name, reputation) \
                          VALUES (%s, %s, %s)",
                         (datetime.now().replace(microsecond=0), current_user, 0))
    return redirect("/")

# QUESTION


@app.route('/new-question')
def route_new_question():
    title_help = True
    database = common.query_handler("""SELECT id, user_name, id FROM users;""")
    return render_template('form_new_question.html', title_help=title_help, form="Question", database=database)


@app.route('/save-Question', methods=['POST'])
def route_save_question():
    if int(request.form["question_id"]) > -1:
        common.query_handler("""UPDATE question SET title=%s, message=%s, image=%s WHERE id=%s;""",
                             (request.form["title"], request.form["Question"], request.form["image"],
                              request.form["question_id"]))
    else:
        common.query_handler("""INSERT INTO question (submission_time, view_number, vote_number, title, message, image, users_id)
                                VALUES(%s,%s,%s,%s,%s,%s,%s);""",
                             (datetime.now().replace(microsecond=0), 0, 0, request.form["title"], request.form["Question"],
                              request.form["image"], request.form["user"]))
    return redirect('/list')


@app.route('/question/<questionid>/')
def route_question_page(questionid=None):
    id_num = questionid
    question_database = common.query_handler("""SELECT question.id, question.submission_time, view_number, vote_number, title, message, image, user_name
                                             FROM question LEFT JOIN users ON users.id=users_id
                                             WHERE question.id=%s""", (id_num,))
    answer_database = common.query_handler("""SELECT answer.id, answer.submission_time, vote_number, question_id, message, image, accepted, user_name
                                            FROM answer LEFT JOIN users ON users.id=users_id WHERE question_id=%s""", (id_num,))
    comment_database = common.query_handler("""SELECT comment.id, question_id, answer_id, comment.submission_time, message, user_name
                                             FROM comment LEFT JOIN users ON users.id=users_id""")
    tag_database = common.query_handler("""SELECT * FROM tag INNER JOIN question_tag
                                           ON tag.id=question_tag.tag_id
                                           WHERE question_tag.question_id=%s;""", (id_num,))
    return render_template('question.html', question_database=question_database, answer_database=answer_database,
                           id_num=id_num, comment_database=comment_database, tag_database=tag_database)


@app.route('/edit-question/<questionid>/')
def route_edit_question(questionid=None):
    edit = True
    id_num = questionid
    database = common.query_handler("SELECT * FROM question WHERE id=%s;", (id_num,))
    return render_template('form_edit_question.html', edit=edit, id_num=id_num, database=database, form="Question")


@app.route('/delete-question/<questionid>/')
def route_delete_question(questionid=None):
    id_num = questionid
    answers = common.query_handler("SELECT id FROM answer WHERE question_id=%s", (id_num,))
    for line in answers:
        common.query_handler("DELETE FROM comment WHERE answer_id=%s", (line["id"],))
    common.query_handler("DELETE FROM question_tag WHERE question_id=%s", (id_num,))
    common.query_handler("DELETE FROM comment WHERE question_id=%s", (id_num,))
    common.query_handler("DELETE FROM answer WHERE question_id=%s", (id_num,))
    common.query_handler("DELETE FROM question WHERE id=%s", (id_num,))
    return redirect('/')


@app.route('/question/<questionid>/vote-up')
def route_upvote_question(questionid=None):
    id_num = questionid
    common.reputation_counter("5", 'question', id_num )
    common.query_handler("UPDATE question SET vote_number = vote_number+1 WHERE id=%s", (id_num,))
    return redirect('/')


@app.route('/question/<questionid>/vote-down')
def route_downvote_question(questionid=None):
    id_num = questionid
    common.reputation_counter("-2", 'question', id_num )
    common.query_handler("UPDATE question SET vote_number = vote_number-1 WHERE id=%s", (id_num,))
    return redirect('/')

# ANSWER


@app.route('/question/<questionid>/new-answer')
def new_answer(questionid):
    id_num = questionid
    add_answer = True
    users_database = common.query_handler("SELECT * FROM users;")
    question_database = common.query_handler("SELECT * FROM question WHERE id=%s", (id_num,))
    return render_template('form_new_answer.html', form="Answer", add_answer=add_answer, id_num=id_num,
                           question_database=question_database, users_database=users_database)


@app.route('/save-Answer', methods=['POST'])
def route_save_answer():
    formdata = request.form
    common.query_handler("""INSERT INTO answer (submission_time, vote_number, question_id, message, image, users_id)
                            VALUES(%s, %s, %s, %s, %s, %s)""",
                         (datetime.now().replace(microsecond=0), 0, formdata['question_id'], formdata['Answer'], formdata['image'], formdata['user']))
    return redirect('/question/' + request.form['question_id'])


@app.route('/delete-answer/<questionid>/<answerid>/')
def route_delete_answer(questionid=None, answerid=None):
    id_num = int(answerid)
    common.query_handler("DELETE FROM comment WHERE answer_id=%s", (id_num,))
    common.query_handler("DELETE FROM answer WHERE id=%s", (id_num,))
    return redirect('/question/'+questionid+'/')


@app.route('/question/<questionid>/<answerid>/vote-up/')
def route_upvote_answer(questionid=None, answerid=None):
    id_num = int(answerid)
    id_question = questionid
    common.reputation_counter('10', 'answer', id_num )
    common.query_handler("UPDATE answer SET vote_number = vote_number+1 WHERE id=%s", (id_num,))
    return redirect('/question/' + id_question + "/")


@app.route('/question/<questionid>/<answerid>/vote-down/')
def route_downvote_answer(questionid=None, answerid=None):
    id_num = answerid
    id_question = questionid
    common.reputation_counter('-2', 'answer', id_num )
    common.query_handler("UPDATE answer SET vote_number = vote_number-1 WHERE id=%s", (id_num,))
    return redirect('/question/' + id_question + "/")


@app.route('/question/<question_id>/<answer_id>/accept-answer')
def accept_answer(question_id, answer_id):
    common.query_handler("UPDATE answer SET accepted='1' WHERE id=%s", (answer_id,))
    common.reputation_counter('15', 'answer', answer_id )
    return redirect("/question/"+question_id+"/")


# COMMENT


@app.route('/question/<questionid>/new-comment')
def new_comment(questionid):
    id_num = questionid
    add_answer = True
    users_database = common.query_handler("SELECT * FROM users;")
    question_database = common.query_handler("SELECT * FROM question WHERE id=%s", (id_num,))
    return render_template('form_new_answer.html', form="Comment", add_answer=add_answer, id_num=id_num,
                           question_database=question_database, users_database=users_database)


@app.route('/answer/<answer_id>/new-comment')
def new_comment_answer(answer_id):
    answer_database = common.query_handler("SELECT * FROM answer WHERE id=%s", (answer_id,))
    users_database = common.query_handler("SELECT * FROM users;")
    return render_template('form_answer_comment.html', form="Comment", answer_database=answer_database,
                           users_database=users_database)


@app.route('/save-answer-Comment', methods=['POST'])
def route_new_comment_answer():
    formdata = request.form
    common.query_handler("""INSERT INTO comment (answer_id, message, submission_time, edited_count, users_id)
                            VALUES(%s, %s, %s, %s, %s)""", (formdata['answer_id'], formdata['Comment'], datetime.now().replace(microsecond=0), 0, formdata['user']))
    questiondata = common.query_handler("SELECT question_id FROM answer WHERE id=%s", (formdata['answer_id'],))
    return redirect('/question/' + str(questiondata[0]["question_id"]))


@app.route('/save-Comment', methods=['POST'])
def route_save_comment():
    formdata = request.form
    common.query_handler("""INSERT INTO comment (question_id, message, submission_time, edited_count, users_id)
                            VALUES(%s, %s, %s, %s, %s)""", (formdata['question_id'],
                         formdata['Comment'], datetime.now().replace(microsecond=0), 0, formdata['user']))
    return redirect('/question/' + request.form['question_id'])


@app.route('/update-Comment', methods=['POST'])
def route_update_comment():
    formdata = request.form
    common.query_handler("""UPDATE comment SET message=%s, edited_count = edited_count + 1, users_id=%s
                            WHERE id=%s""", (formdata['Comment'], formdata['user'], formdata['comment_id']))
    return redirect('/question/' + request.form['question_id'])


@app.route('/comments/<comment_id>/edit')
def edit_comment(comment_id):
    answer_comment = False
    question_database = common.query_handler("""SELECT title, question.id AS question_id FROM question
                                                INNER JOIN comment ON question.id=comment.question_id
                                                WHERE comment.id=%s""", (comment_id,))
    answer_database = common.query_handler("""SELECT answer.message AS message, answer.question_id
                                              AS question_id FROM answer
                                              INNER JOIN comment ON answer.id=comment.answer_id
                                              WHERE comment.id=%s""", (comment_id,))
    comment_database = common.query_handler("""SELECT comment.id, question_id, answer_id, message, comment.submission_time, edited_count, users_id, user_name
                                                FROM comment LEFT JOIN users
                                                ON users_id=users.id
                                                WHERE comment.id=%s""", (comment_id,))
    if comment_database[0]['question_id'] is None:
        answer_comment = True
    return render_template("form_edit_comment.html", answer_comment=answer_comment, form="Comment",
                           comment_database=comment_database, question_database=question_database,
                           answer_database=answer_database)


@app.route('/comments/<comment_id>/delete')
def delete_comment(comment_id):
    question = common.query_handler("SELECT question_id, answer_id FROM comment WHERE id=%s", (int(comment_id),))
    common.query_handler("DELETE FROM comment WHERE id=%s", (comment_id,))
    if question[0]["question_id"] is None:
        answer = common.query_handler("SELECT question_id FROM answer WHERE id=%s", (question[0]["answer_id"],))
        return redirect('/question/'+str(answer[0]["question_id"])+'/')
    return redirect('/question/'+str(question[0]["question_id"])+'/')

# TAG


@app.route("/question/<questionid>/new-tag")
def new_tag(questionid):
    question_database = common.query_handler("SELECT * FROM question WHERE id=%s", (questionid,))
    tag_database = common.query_handler("SELECT * FROM tag")
    return render_template("new_tag.html", question_database=question_database, tag_database=tag_database)


@app.route('/save-tag', methods=['POST'])
def route_save_tag():
    if request.form["tags"] == "None":
        tagid = common.query_handler('SELECT * FROM tag WHERE name=%s', (request.form['Tag'],))
        if tagid[0]['name'] != request.form['Tag']:
            common.query_handler("""INSERT INTO tag (name) VALUES(%s)""", (request.form['Tag'],))
        try:
            common.query_handler("""INSERT INTO question_tag (question_id, tag_id) VALUES(%s, %s)""",
                                 (request.form['question_id'], tagid[0]['id']))
        except:
            pass
    else:
        tagid = common.query_handler('SELECT * FROM tag WHERE name=%s', (request.form['tags'],))
        try:
            common.query_handler("""INSERT INTO question_tag (question_id, tag_id) VALUES(%s, %s);""",
                                 (request.form['question_id'], tagid[0]['id']))
        except:
            pass
    return redirect('/question/' + request.form['question_id'])


@app.route("/question/<question_id>/tag/<tag_id>/delete")
def route_delete_tag(question_id, tag_id):
    common.query_handler("DELETE FROM question_tag WHERE question_id=%s AND tag_id=%s", (question_id, tag_id))
    return redirect('/question/'+question_id+'/')


@app.route("/list/sort/<condition>/<direction>")
def sort_questions(condition, direction):
    sort = True
    search = False
    if condition == "time":
        if direction == "ASC":
            database = common.query_handler("SELECT * FROM question ORDER BY submission_time ASC")
        elif direction == "DESC":
            sort = False
            database = common.query_handler("SELECT * FROM question ORDER BY submission_time DESC")
    elif condition == "view":
        if direction == "ASC":
            database = common.query_handler("SELECT * FROM question ORDER BY view_number ASC")
        elif direction == "DESC":
            sort = False
            database = common.query_handler("SELECT * FROM question ORDER BY view_number DESC")
    elif condition == "vote":
        if direction == "ASC":
            database = common.query_handler("SELECT * FROM question ORDER BY vote_number ASC")
        elif direction == "DESC":
            sort = False
            database = common.query_handler("SELECT * FROM question ORDER BY vote_number DESC")
    return render_template("list.html", database=database, search=search, sort=sort)


if __name__ == "__main__":
    app.secret_key = "whoeventriestoguessthis"
    app.run(
        debug=True,
        port=5000
    )
