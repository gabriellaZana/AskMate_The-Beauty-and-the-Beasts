from flask import Flask, render_template, redirect, request, session, url_for
import common

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def index():
    database = common.import_story("data/question.csv")
    return render_template("list.html", database=database)


@app.route('/save-answer', methods=['POST'])
def route_save_answer():
    pass


@app.route('/question/<question-id>/new-answer')
def new_answer():
    pass


if __name__ == "__main__":
    app.secret_key = "whoeventriestoguessthis"
    app.run(
        debug=True,
        port=5000
    )