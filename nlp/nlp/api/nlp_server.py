from flask import request
import nlp

@nlp.app.route('/', methods=["GET"])
def base():
    return "Welcome to the NLP server!"

@nlp.app.route('/receive/email/', methods=["POST"])
def receive_email():
    print(request.form)
    print(request.form.get("body"))
    return "" # we essentially don't care about the interface of the NLP server

@nlp.app.route('/receive/voice/', methods=["POST"])
def receive_voice():
    print(request.form.get('filename'))
    return "" # we essentially don't care about the interface of the NLP server