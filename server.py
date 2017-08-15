from flask import Flask, render_template, redirect, request, session, url_for
import common

app = Flask(__name__)


@app.route('/question/<questionid>')
def route_question_page(questionid=None):
    id_pos = int(id)
    q_list = common.import_story("question.csv")
    a_list = common.import_story("answer.csv")

    return render_template('question.html', q_list=q_list, a_list=a_list, id_pos=id_pos)


@app.route('/save-answer', methods=['POST'])
def route_save_answer():
    pass


@app.route('/question/<question-id>/new-answer')
def new_answer():
    return render_template('form.html', form="Answer")


if __name__ == "__main__":
    app.secret_key = "whoeventriestoguessthis"
    app.run(
        debug=True,
        port=5000
    )
