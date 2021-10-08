import flask
from flask import json, request
import backend
import backend.ezgmail as ezgmail

@backend.app.route('/', methods=["GET"])
def index():
    return "helloworld"

@backend.app.route('/api/email/', methods=["GET"])
def email():
    email_id = request.args.get("id", default=-1, type=int)
    message_dict = _email(email_id)
    if message_dict:
        return flask.jsonify(message_dict)
    else:
        return flask.jsonify({
            "error": "IndexError"
        })


def _email(email_id):
    recent_mails = ezgmail.recent()
    try:
        message: ezgmail.GmailMessage = recent_mails[email_id].messages[0]
    except IndexError:
        return None
    message_dict = {
        "id": email_id,
        "from": message.sender,
        "to": message.recipient.split(","),
        "subject": message.subject,
        "time": message.timestamp,
        "body": message.body
    }
    return message_dict