from flask import Flask, render_template, redirect, request, session, url_for
import common
import time
from datetime import datetime
import queries
question_keys = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
answer_keys = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


app = Flask(__name__)

# LIST


@app.route("/")
def latest_5():
    search = False
    database = queries.index()
    return render_template("list.html", database=database, search=search)


@app.route("/list")
def index():
    sort = None
    search = False
    database = queries.indexlist()
    return render_template("list.html", database=database, search=search)


@app.route("/all-users")
def all_users():
    database = queries.all_users()
    return render_template("user.html", database=database)


@app.route("/viewcount/<questionid>", methods=["POST"])
def viewcount(questionid):
    table = queries.viewcount(questionid)
    return redirect('/question/' + questionid + "/")


@app.route("/search", methods=["POST"])
def search():
    search = True
    form_data = request.form
    replacement = {"search": form_data["asksearch"], "marks": '<span class="fancy">{}</span>'.format(form_data['asksearch'])}
    questions = queries.search(form_data) 
    return render_template("list.html", phrase=form_data["asksearch"], question_database=question_database,
                           questions=questions, search=search)


@app.route('/tags')
def route_tags():
    database = queries.tags()
    return render_template("tags.html", database=database)


# REGISTRASION

@app.route('/registration')
def route_registration():
    return render_template("form_registration.html", isValid=True)


@app.route('/save-user', methods=["POST"])
def route_save_user():
    existing_users = queries.usernames()
    current_user = request.form["username"]
    for line in existing_users:
        if line["user_name"] == current_user:
            return render_template("form_registration.html", isValid=False)
    queries.insert_users(current_user)
    return redirect("/")

# QUESTION


@app.route('/new-question')
def route_new_question():
    title_help = True
    database = queries.username_id()
    return render_template('form_new_question.html', title_help=title_help, form="Question", database=database)


@app.route('/save-Question', methods=['POST'])
def route_save_question():
    formdata = request.form
    if int(formdata["question_id"]) > -1:
        queries.update_question(formdata)
    else:
        queries.new_question(formdata)
    return redirect('/list')


@app.route('/question/<questionid>/')
def route_question_page(questionid=None):
    id_num = questionid
    question_database = queries.select_question(id_num)
    answer_database = queries.select_answer(id_num)
    comment_database = queries.select_comment()
    tag_database = queries.select_tag(id_num)
    return render_template('question.html', question_database=question_database, answer_database=answer_database,
                           id_num=id_num, comment_database=comment_database, tag_database=tag_database)


@app.route('/edit-question/<questionid>/')
def route_edit_question(questionid=None):
    edit = True
    id_num = questionid
    database = queries.question_by_id(id_num)
    return render_template('form_edit_question.html', edit=edit, id_num=id_num, database=database, form="Question")


@app.route('/delete-question/<questionid>/')
def route_delete_question(questionid=None):
    id_num = questionid
    answers = queries.answer_on_question(id_num)
    for line in answers:
        queries.delete_comment_from_answer(line)
    queries.delete_question(id_num)
    return redirect('/')


@app.route('/question/<questionid>/vote-up')
def route_upvote_question(questionid=None):
    id_num = questionid
    common.reputation_counter("5", 'question', id_num )
    queries.question_vote_up(id_num)
    return redirect('/')


@app.route('/question/<questionid>/vote-down')
def route_downvote_question(questionid=None):
    id_num = questionid
    common.reputation_counter("-2", 'question', id_num )
    queries.question_vote_down(id_num)
    return redirect('/')

# ANSWER


@app.route('/question/<questionid>/new-answer')
def new_answer(questionid):
    id_num = questionid
    add_answer = True
    users_database = queries.select_all_users()
    question_database = queries.question_by_id(id_num)
    return render_template('form_new_answer.html', form="Answer", add_answer=add_answer, id_num=id_num,
                           question_database=question_database, users_database=users_database)


@app.route('/save-Answer', methods=['POST'])
def route_save_answer():
    formdata = request.form
    queries.new_answer(formdata)
    return redirect('/question/' + request.form['question_id'])


@app.route('/delete-answer/<questionid>/<answerid>/')
def route_delete_answer(questionid=None, answerid=None):
    id_num = int(answerid)
    queries.delete_answer(id_num)
    return redirect('/question/'+questionid+'/')


@app.route('/question/<questionid>/<answerid>/vote-up/')
def route_upvote_answer(questionid=None, answerid=None):
    id_num = int(answerid)
    id_question = questionid
    common.reputation_counter('10', 'answer', id_num )
    queries.answer_vote_up(id_num)
    return redirect('/question/' + id_question + "/")


@app.route('/question/<questionid>/<answerid>/vote-down/')
def route_downvote_answer(questionid=None, answerid=None):
    id_num = answerid
    id_question = questionid
    common.reputation_counter('-2', 'answer', id_num )
    queries.answer_vote_down(id_num)
    return redirect('/question/' + id_question + "/")


@app.route('/question/<question_id>/<answer_id>/accept-answer')
def accept_answer(question_id, answer_id):
    queries.accept_answer(answer_id)
    common.reputation_counter('15', 'answer', answer_id )
    return redirect("/question/"+question_id+"/")


# COMMENT


@app.route('/question/<questionid>/new-comment')
def new_comment(questionid):
    id_num = questionid
    add_answer = True
    users_database = queries.select_all_users()
    question_database = queries.question_by_id(id_num)
    return render_template('form_new_answer.html', form="Comment", add_answer=add_answer, id_num=id_num,
                           question_database=question_database, users_database=users_database)


@app.route('/answer/<answer_id>/new-comment')
def new_comment_answer(answer_id):
    answer_database = queries.answer_by_id(answer_id)
    users_database = queries.select_all_users()
    return render_template('form_answer_comment.html', form="Comment", answer_database=answer_database,
                           users_database=users_database)


@app.route('/save-answer-Comment', methods=['POST'])
def route_new_comment_answer():
    formdata = request.form
    queries.comment_on_answer(formdata)
    questiondata = queries.questionid_to_answer(formdata)
    return redirect('/question/' + str(questiondata[0]["question_id"]))


@app.route('/save-Comment', methods=['POST'])
def route_save_comment():
    formdata = request.form
    queries.save_comment(formdata)
    return redirect('/question/' + request.form['question_id'])


@app.route('/update-Comment', methods=['POST'])
def route_update_comment():
    formdata = request.form
    queries.update_comment(formdata)
    return redirect('/question/' + request.form['question_id'])


@app.route('/comments/<comment_id>/edit')
def edit_comment(comment_id):
    answer_comment = False
    question_database = queries.question_comment(comment_id)
    answer_database = queries.answer_comment(comment_id)
    comment_database = queries.comment_user(comment_id)
    if comment_database[0]['question_id'] is None:
        answer_comment = True
    return render_template("form_edit_comment.html", answer_comment=answer_comment, form="Comment",
                           comment_database=comment_database, question_database=question_database,
                           answer_database=answer_database)


@app.route('/comments/<comment_id>/delete')
def delete_comment(comment_id):
    question = queries.question_to_comment(comment_id)
    queries.delete_comment(comment_id)
    if question[0]["question_id"] is None:
        answer = queries.questionid_to_answer_from_dict(question)
        return redirect('/question/'+str(answer[0]["question_id"])+'/')
    return redirect('/question/'+str(question[0]["question_id"])+'/')

# TAG


@app.route("/question/<questionid>/new-tag")
def new_tag(questionid):
    question_database = queries.question_by_id(questionid)
    tag_database = queries.select_all_tags()
    return render_template("new_tag.html", question_database=question_database, tag_database=tag_database)


@app.route('/save-tag', methods=['POST'])
def route_save_tag():
    if request.form["tags"] == "None":
        tagid = queries.tag_by_id(request.form, 'Tag')
        if tagid == []:
            queries.insert_tag_name(request.form)
        try:
            tagid = queries.tag_by_id(request.form, 'Tag')
            queries.insert_tag_to_question(request.form, tagid)
        except:
            pass
    else:
        tagid = queries.tag_by_id(request.form, 'tags')
        try:
            queries.insert_tag_to_question(request.form, tagid)
        except:
            pass
    return redirect('/question/' + request.form['question_id'])


@app.route("/question/<question_id>/tag/<tag_id>/delete")
def route_delete_tag(question_id, tag_id):
    queries.delete_tag(question_id, tag_id)
    return redirect('/question/'+question_id+'/')


@app.route("/list/sort/<condition>/<direction>")
def sort_questions(condition, direction):
    sort = True
    search = False
    if condition == "time":
        if direction == "ASC":
            database = queries.sort_by_condition("submission_time ASC")
        elif direction == "DESC":
            sort = False
            database = queries.sort_by_condition("submission_time DESC")
    elif condition == "view":
        if direction == "ASC":
            database = queries.sort_by_condition("view_number ASC")
        elif direction == "DESC":
            sort = False
            database = queries.sort_by_condition("view_number DESC")
    elif condition == "vote":
        if direction == "ASC":
            database = queries.sort_by_condition("vote_number ASC")
        elif direction == "DESC":
            sort = False
            database = queries.sort_by_condition("vote_number DESC")
    return render_template("list.html", questions=database, search=search, sort=sort)


@app.route("/form_user/<user_id>/sort/<condition>/<direction>")
def sort_user_questions(condition, direction, user_id):
    sort = True
    search = False
    if condition == "time":
        if direction == "ASC":
            database = queries.user_sort("submission_time ASC", user_id)
        elif direction == "DESC":
            sort = False
            database = queries.user_sort("submission_time DESC", user_id)
    elif condition == "view":
        if direction == "ASC":
            database = queries.user_sort("view_number ASC", user_id)
        elif direction == "DESC":
            sort = False
            database = queries.user_sort("view_number DESC", user_id)
    elif condition == "vote":
        if direction == "ASC":
            database = queries.user_sort("vote_number ASC", user_id)
        elif direction == "DESC":
            sort = False
            database = queries.user_sort("vote_number DESC", user_id)
    answers = queries.answer_to_userid(user_id)
    comments = queries.comment_to_userid(user_id)
    users = queries.user_by_id(user_id)
    return render_template("form_user.html", questions=database, sort=sort, answers=answers, comments=comments, users=users)


@app.route("/all-users/<direction>")
def sort_users(direction):
    sort = True
    if direction == "ASC":
        database = queries.sort_users("user_name ASC")
    elif direction == "DESC":
        sort = False
        database = queries.sort_users("user_name DESC")
    return render_template("user.html", database=database, sort=sort)


@app.route("/user/<user_id>")
def user_activity(user_id):
    users = queries.user_by_id(user_id)
    questions = queries.question_to_userid(user_id)
    answers = queries.answer_to_userid(user_id)
    comments = queries.comment_to_userid(user_id)
    return render_template("form_user.html", questions=questions, answers=answers, comments=comments, users=users)


if __name__ == "__main__":
    app.secret_key = "whoeventriestoguessthis"
    app.run(
        debug=True,
        port=5000
    )
    
