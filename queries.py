from flask import Flask, render_template, redirect, request, session, url_for
import common
import time
from datetime import datetime

# LIST


# 1 /
def index():
    return common.query_handler("""SELECT question.id, question.submission_time, view_number,
                                        vote_number, title, message, image, users_id, user_name, reputation
                                    FROM question
                                    LEFT JOIN users ON users.id=users_id
                                    ORDER BY question.submission_time DESC LIMIT 5;""")


# 2 /list
def indexlist():
    return common.query_handler("""SELECT question.id, question.submission_time, view_number,
                                          vote_number, title, message, image, users_id, user_name, reputation
                                    FROM question
                                    LEFT JOIN users ON users.id=users_id;""")


# 3 /all-users
def all_users():
    return common.query_handler("SELECT * FROM users;")


# 4 /viewcount/<questionid>
def viewcount(questionid):
    return common.query_handler("UPDATE question SET view_number = view_number + 1 WHERE id=%s", (questionid,))


# 5 /search
def search(replacement):
    return common.query_handler("""SELECT DISTINCT question.id, question.users_id, user_name,
                                                    question.submission_time, question.view_number,
                                                    question.vote_number, question.image, answer.question_id,
                                                    Replace(question.title, %(search)s, %(marks)s) AS title, 
                                                    Replace(question.message, %(search)s, %(marks)s) AS message
                                                FROM question
                                                  LEFT JOIN users ON question.users_id=users.id
                                                  FULL JOIN answer ON question.id = answer.question_id
                                                WHERE question.title ILIKE '%%' || %(search)s || '%%'
                                                  OR answer.message ILIKE '%%' || %(search)s || '%%'
                                                  OR question.message ILIKE '%%' || %(search)s || '%%' ;""",replacement)


def question_user():
    return common.query_handler("""SELECT question.id, title, message, user_name, question.submission_time, view_number,
                                            vote_number, image FROM question LEFT JOIN users ON users.id=users_id;""")


# 6 /tags
def tags():
    return common.query_handler("SELECT name, COUNT(question_id) AS question_number \
                                     FROM tag JOIN question_tag ON tag.id=question_tag.tag_id \
                                     GROUP BY name")

# REGISTRASION


# 1 /save-user
def usernames():
    return common.query_handler("SELECT user_name FROM users")


def insert_users(current_user):
    common.query_handler("INSERT INTO users (submission_time, user_name, reputation) \
                          VALUES (%s, %s, %s)",
                         (datetime.now().replace(microsecond=0), current_user, 0))

# QUESTION


# 1 /new-question
def username_id():
    return common.query_handler("""SELECT id, user_name, id FROM users;""")


# 2 /save-Question
def update_question(formdata):
    common.query_handler("""UPDATE question SET title=%s, message=%s, image=%s WHERE id=%s;""",
                         (formdata["title"], formdata["Question"], formdata["image"],
                          formdata["question_id"]))


def new_question(formdata):
    common.query_handler("""INSERT INTO question (submission_time, view_number, vote_number, title, message, image, users_id)
                                VALUES(%s,%s,%s,%s,%s,%s,%s);""",
                         (datetime.now().replace(microsecond=0), 0, 0, formdata["title"], formdata["Question"],
                          formdata["image"], formdata["user"]))


# 3 /question/<questionid>/
def select_question(questionid):
    return common.query_handler("""SELECT question.id, question.submission_time, view_number, vote_number, title, message, image, user_name
                                             FROM question LEFT JOIN users ON users.id=users_id
                                             WHERE question.id=%s""", (questionid,))


def select_answer(questionid):
    return common.query_handler("""SELECT answer.id, answer.submission_time, vote_number, question_id, message, image, accepted, users_id, user_name
                                    FROM answer LEFT JOIN users ON users.id=users_id
                                    WHERE question_id=%s""", (questionid,))


def select_comment():
    return common.query_handler("""SELECT comment.id, question_id, answer_id, comment.submission_time, message, users_id, user_name
                                             FROM comment LEFT JOIN users ON users.id=users_id""")


def select_tag(questionid):    
    return common.query_handler("""SELECT * FROM tag INNER JOIN question_tag
                                           ON tag.id=question_tag.tag_id
                                           WHERE question_tag.question_id=%s;""", (questionid,))


# 4 /edit-question/<questionid>/
def question_by_id(questionid):
    return common.query_handler("SELECT * FROM question WHERE id=%s;", (questionid,))


# 5 /delete-question/<questionid>
def answer_on_question(questionid):
    return common.query_handler("SELECT id FROM answer WHERE question_id=%s", (questionid,))


def delete_comment_from_answer(line):
    common.query_handler("DELETE FROM comment WHERE answer_id=%s", (line["id"],))


def delete_question(questionid):
    common.query_handler("DELETE FROM question_tag WHERE question_id=%s", (questionid,))
    common.query_handler("DELETE FROM comment WHERE question_id=%s", (questionid,))
    common.query_handler("DELETE FROM answer WHERE question_id=%s", (questionid,))
    common.query_handler("DELETE FROM question WHERE id=%s", (questionid,))


# 6 /question/<questionid>/vote-up
def question_vote_up(questionid):
    common.query_handler("UPDATE question SET vote_number = vote_number+1 WHERE id=%s", (questionid,))


# 7 /question/<questionid>/vote-down
def question_vote_down(questionid):
    common.query_handler("UPDATE question SET vote_number = vote_number-1 WHERE id=%s", (questionid,))

# ANSWER


# 1 /question/<questionid>/new-answer
def select_all_users():
    return common.query_handler("SELECT * FROM users;")


# 2 /save-Answer
def new_answer(formdata):
    common.query_handler("""INSERT INTO answer (submission_time, vote_number, question_id, message, image, users_id)
                            VALUES(%s, %s, %s, %s, %s, %s)""",
                         (datetime.now().replace(microsecond=0), 0,
                          formdata['question_id'], formdata['Answer'], formdata['image'], formdata['user']))


# 3 /delete-answer/<questionid>/<answerid>/
def delete_answer(answerid):
    common.query_handler("DELETE FROM comment WHERE answer_id=%s", (answerid,))
    common.query_handler("DELETE FROM answer WHERE id=%s", (answerid,))


# 4 /question/<questionid>/<answerid>/vote-up/
def answer_vote_up(answerid):
    common.query_handler("UPDATE answer SET vote_number = vote_number+1 WHERE id=%s", (answerid,))


# 5 /question/<questionid>/<answerid>/vote-down/
def answer_vote_down(answerid):
    common.query_handler("UPDATE answer SET vote_number = vote_number-1 WHERE id=%s", (answerid,))


# 6 /question/<question_id>/<answer_id>/accept-answer
def accept_answer(answerid):
    common.query_handler("UPDATE answer SET accepted='1' WHERE id=%s", (answerid,))


# COMMENT


# 2 /answer/<answer_id>/new-comment
def answer_by_id(answerid):
    return common.query_handler("SELECT * FROM answer WHERE id=%s", (answerid,))


# 3 /save-answer-Comment
def comment_on_answer(formdata):
    common.query_handler("""INSERT INTO comment (answer_id, message, submission_time, edited_count, users_id)
                            VALUES(%s, %s, %s, %s, %s)""", (formdata['answer_id'],
                                                            formdata['Comment'],
                                                            datetime.now().replace(microsecond=0), 0, formdata['user']))


def questionid_to_answer(formdata):    
    return common.query_handler("SELECT question_id FROM answer WHERE id=%s", (formdata['answer_id'],))


# 4 /save-Comment
def save_comment(formdata):
    common.query_handler("""INSERT INTO comment (question_id, message, submission_time, edited_count, users_id)
                            VALUES(%s, %s, %s, %s, %s)""", (formdata['question_id'],
                         formdata['Comment'], datetime.now().replace(microsecond=0), 0, formdata['user']))


# 5 /update-Comment
def update_comment(formdata):
    common.query_handler("""UPDATE comment SET message=%s, edited_count = edited_count + 1, users_id=%s
                            WHERE id=%s""", (formdata['Comment'], formdata['user'], formdata['comment_id']))


# 6 /comments/<comment_id>/edit
def question_comment(comment_id):
    return common.query_handler("""SELECT title, question.id AS question_id FROM question
                                                INNER JOIN comment ON question.id=comment.question_id
                                                WHERE comment.id=%s""", (comment_id,))


def answer_comment(comment_id):    
    return common.query_handler("""SELECT answer.message AS message, answer.question_id
                                              AS question_id FROM answer
                                              INNER JOIN comment ON answer.id=comment.answer_id
                                              WHERE comment.id=%s""", (comment_id,))


def comment_user(comment_id):    
    return common.query_handler("""SELECT comment.id, question_id, answer_id, message, comment.submission_time, edited_count, users_id, user_name
                                                FROM comment LEFT JOIN users
                                                ON users_id=users.id
                                                WHERE comment.id=%s""", (comment_id,))


# 7 /comments/<comment_id>/delete
def question_to_comment(comment_id):
    return common.query_handler("SELECT question_id, answer_id FROM comment WHERE id=%s", (int(comment_id),))


def delete_comment(comment_id):
    common.query_handler("DELETE FROM comment WHERE id=%s", (comment_id,))


def questionid_to_answer_from_dict(question):
    return common.query_handler("SELECT question_id FROM answer WHERE id=%s", (question[0]["answer_id"],))

# TAG


# 1 /question/<questionid>/new-tag
def select_all_tags():    
    return common.query_handler("SELECT * FROM tag")


# 2 /save-tag
def tag_by_id(formdata, tagkey):
    return common.query_handler('SELECT * FROM tag WHERE name=%s', (formdata[tagkey],))


def insert_tag_name(formdata):
    common.query_handler("""INSERT INTO tag (name) VALUES(%s)""", (formdata['Tag'],))


def insert_tag_to_question(formdata, tagid):
    common.query_handler("""INSERT INTO question_tag (question_id, tag_id)
                            VALUES(%s, %s)""", (formdata['question_id'], tagid[0]['id']))


# 3 /question/<question_id>/tag/<tag_id>/delete
def delete_tag(questionid, tag_id):
    common.query_handler("DELETE FROM question_tag WHERE question_id=%s AND tag_id=%s", (questionid, tag_id))


# 4 /list/sort/<condition>/<direction>
def sort_by_condition(condition):
    condition_list = ["submission_time ASC", "submission_time DESC", "view_number ASC",
                      "view_number DESC", "vote_number ASC", "vote_number DESC"]
    if condition in condition_list:
        return common.query_handler("""SELECT question.id, title, message, user_name, question.submission_time,
                                        view_number, vote_number, image FROM question LEFT JOIN users
                                       ON users.id=users_id ORDER BY """ + condition)
    else:
        return common.query_handler("""SELECT question.id, title, message, user_name, question.submission_time,
                                        view_number, vote_number, image
                                       FROM question LEFT JOIN users ON users.id=users_id
                                       ORDER BY submission_time ASC""")


# 5 /form_user/<user_id>/sort/<condition>/<direction>
def user_sort(condition, user_id):
    condition_list = ["submission_time ASC", "submission_time DESC", "view_number ASC",
                      "view_number DESC", "vote_number ASC", "vote_number DESC"]
    if condition in condition_list:
        return common.query_handler("SELECT * FROM question WHERE users_id=%s ORDER BY " + condition, (user_id,))
    else:
        return common.query_handler("SELECT * FROM question WHERE users_id=%s ORDER BY submission_time ASC", (user_id,))


def answer_to_userid(user_id):
    return common.query_handler("""SELECT * FROM answer
                                    WHERE users_id=%s""", (user_id,))


def comment_to_userid(user_id):
    return common.query_handler("""SELECT * FROM comment
                                    WHERE users_id=%s""", (user_id,))


def user_by_id(user_id):
    return common.query_handler("""SELECT * FROM users
                                WHERE id=%s""", (user_id,))


# 7 /all-users/<direction>
def sort_users(condition):
    condition_list = ["user_name ASC", "user_name DESC"]
    if condition in condition_list:
        return common.query_handler("SELECT * FROM users ORDER BY " + condition)
    else:
        return common.query_handler("""SELECT * FROM users ORDER BY user_name ASC;""")


# 6 /user/<user_id>

def question_to_userid(user_id):
    return common.query_handler("""SELECT * FROM question
                                        WHERE users_id=%s""", (user_id,))


def answer_question_to_userid(user_id):
    return common.query_handler("""SELECT answer.submission_time, answer.vote_number,answer.question_id,
                                             answer.message, answer.image, question.title AS quest
                                      FROM answer
                                      JOIN question ON question_id=question.id
                                      WHERE answer.users_id=%s""", (user_id,))


def comment_question_answer_to_userid(user_id):
    return common.query_handler("""SELECT comment.question_id AS questid, comment.submission_time, comment.message,
                                              answer.message AS ansme, question.title AS quest, answer.question_id
                                       FROM comment
                                       LEFT JOIN question ON comment.question_id=question.id
                                       LEFT JOIN answer ON comment.answer_id=answer.id
                                       WHERE comment.users_id=%s""", (user_id,))
