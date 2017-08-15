from flask import Flask, render_template, redirect, request, session, url_for

app = Flask(__name__)


@app.route('/save-answer', methods=['POST'])
def route_save_answer(questionid):
    table = []
    table.append(get_last_row("data/anwser.csv"))
    table.append(time.time())
    table.append("0")
    table.append(questionid)
    table.append(request.form[Answer])
    table.append("image")
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
