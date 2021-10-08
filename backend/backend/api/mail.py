from webbrowser import get
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
    message_dict = _email_to_dict(email_id)
    if message_dict:
        return flask.jsonify(message_dict)
    else:
        return flask.jsonify({
            "error": "IndexError"
        })


@backend.app.route("/api/command/", methods=["GET"])
def command():
    if request.is_json:
        req_json = request.get_json()
        req_dict = json.loads(req_json) if isinstance(req_json, str) else req_json
        try:
            _command(req_dict["id"], req_dict["command"], req_dict["args"])
        except NotImplementedError as e:
            return flask.jsonify({
                'error': str(e)
            })
        return flask.jsonify({
            'success': True
        })
    else:
        return flask.jsonify({
            'error': 'Invalid post, should be json.'
        })


def _email_to_dict(email_id):
    try:
        message = get_message(email_id)
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


def _command(email_id, command, args={}):
    """Parse and execute the command.

    List of current avaliable commands:
    1. `read` - no args
    2. `unread` - no args
    """
    m = get_message(email_id)
    if command == 'read':
        m.markAsRead()
    elif command == 'unread':
        m.markAsUnread()
    else:
        raise NotImplementedError("Not support command `{}`".format(command))


def get_message(email_id):
    """TODO - Need absolute index of all INBOX messages."""
    recent_mails = ezgmail.recent()
    message: ezgmail.GmailMessage = recent_mails[email_id].messages[0]
    return message
