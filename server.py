from flask import Flask, render_template, redirect, request, session, url_for

app = Flask(__name__)


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