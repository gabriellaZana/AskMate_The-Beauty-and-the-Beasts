from flask import Flask, render_template, redirect, request, session, url_for

app = Flask(__name__)

if __name__=="__main__":
    app.secret_key = "whoeventriestoguessthis"
    app.run(
        debug=True,
        port=5000
    )