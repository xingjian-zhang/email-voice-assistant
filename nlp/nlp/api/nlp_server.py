import nlp
from flask import request
import requests


@nlp.app.route('/', methods=["GET"])
def base():
    return "Welcome to the NLP server!"


@nlp.app.route('/voice/', methods=["GET"])
def parse_voice():
    path = request.args.get('path')
    # 1. speech 2 text
    text = _speech_to_text(path)
    # 2. parse command & email_id
    command = "read"
    email_id = -1
    args = {}
    # 3. send command to backend
    _send_command(command, email_id, args)
    return text

# @nlp.app.route('/send/', methods=["GET"])


def _send_command(command, email_id, args):
    email_dict = _get_email(email_id) # for other functionalities
    command_dict = {
        "id": email_id,
        "command": command,
        "args": args
    }
    requests.get(
        f"http://localhost:{nlp.app.config['BACKEND_SERVER_PORT']}/api/command/", json=command_dict)
    return command_dict


def _get_email(email_id):
    return requests.get(f"http://localhost:{nlp.app.config['BACKEND_SERVER_PORT']}/api/email/").json()


def _speech_to_text(path):
    return "hello"
