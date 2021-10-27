import flask
from flask import request
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
        message_dict["success"] = True
        return flask.jsonify(message_dict)
    else:
        return flask.jsonify({
            'success': False,
            "error": "IndexError"
        }), 400


@backend.app.route("/api/command/", methods=["GET"])
def command():
    req_dict = request.get_json(force=True)  # directly a dict
    print(req_dict)
    try:
        response = _command(
            req_dict["id"], req_dict["command"], req_dict["args"])
    except NotImplementedError as e:
        return flask.jsonify({
            'success': False,
            'error': str(e)
        }), 400
    return flask.jsonify({
        'success': True,
        'response': response
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
    3. `spam` - no args
    4. `delete` - no args
    5. `search`
        - `query`: a string, see details @ https://support.google.com/mail/answer/7190?hl=en
    TODO:
    1. `forward` to a list of users with/without new content
    2. `reply`
    """
    m = get_message(email_id)
    response = None
    if command == 'read':
        m.markAsRead()
    elif command == 'unread':
        m.markAsUnread()
    elif command == 'spam':
        m.markAsSpam()
    elif command == 'delete':
        m.trash()
    elif command == 'search':
        query = args["query"]
        results = ezgmail.search(query)
        # REVIEW - Only extract the first mail of threads
        response = [_email_to_dict(mail[0]) for mail in results]
    elif command == 'show':
        response =  _email_to_dict(email_id)
    else:
        raise NotImplementedError("Not support command `{}`".format(command))
    return response


def get_message(email_id):
    """TODO - Need absolute index of all INBOX messages."""
    try:
        recent_mails = ezgmail.recent(maxResults=9999)
        message: ezgmail.GmailMessage = recent_mails[email_id].messages[0]
    except IndentationError:
        return None
    return message
