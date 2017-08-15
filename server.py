from flask import Flask, render_template, redirect, request, session, url_for
import common

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def index():
    database = import_data("database.csv")  # common import
    return render_template("list.html", database=database)


if __name__=="__main__":
    app.secret_key = "whoeventriestoguessthis"
    app.run(
        debug=True,
        port=5000
    )