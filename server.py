from flask import Flask, render_template, redirect, request, session, url_for
import common

app = Flask(__name__)


@app.route('/save-question', methods=['POST'])
def route_save_question():
    formdata = request.form
    table = import_story("question.csv")
    create_list = []
    create_list.append(id_generator("question.csv"))

    return render_template('list.html', form="question")


@app.route('/new-question')
def route_new_question():
    render_template('form.html')


@app.route("/")
@app.route("/list")
def index():
    database = common.import_story("data/question.csv")
    return render_template("list.html", database=database)


@app.route('/question/<id>')
def route_question_page(id=None):
    id_pos = int(id)
    q_list = common.import_story("question.csv")
    a_list = common.import_story("answer.csv")

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
    table = import_story("data/answer.csv")
    table.append(data)
    export_story("data/answer.csv", table)
    return render_template('/question/<questionid>')


@app.route('/question/<questionid>/new-answer')
def new_answer(questionid):
    return render_template('form.html', form="Answer")


if __name__ == "__main__":
    app.secret_key = "whoeventriestoguessthis"
    app.run(
        debug=True,
        port=5000
    )
