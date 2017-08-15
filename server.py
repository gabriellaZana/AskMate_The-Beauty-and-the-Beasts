from flask import Flask, render_template, redirect, request, session, url_for
import common

app = Flask(__name__)


@app.route('/question/<id>')
def route_question_page():
    id_pos = int(id)
    q_list = common.import_story("question.csv")
    a_list = common.import_story("answer.csv")

    return render_template('question.html', q_list=q_list, a_list=a_list, id_pos=id_pos)



if __name__=="__main__":
    app.secret_key = "whoeventriestoguessthis"
    app.run(
        debug=True,
        port=5000
    )