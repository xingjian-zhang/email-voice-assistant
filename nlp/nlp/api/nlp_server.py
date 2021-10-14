from flask import request
import nlp
import requests

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

@nlp.app.route('/send/', methods=["GET"])
def send_command():
    email_id = -1
    command = request.args.get("command", default='read', type=str)
    args = {}
    command_dict = {
        "id": email_id,
        "command": command,
        "args": args
    }
    requests.post(f"http://localhost:{nlp.app.config['BACKEND_SERVER_PORT']}/api/command/", json=command_dict)
    return command_dict
    