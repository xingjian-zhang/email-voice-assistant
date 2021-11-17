from google.cloud import dialogflow
import nlp
import requests

PROJECT_ID = "test-conv-ai-1011"

class Dialogflow_session:
    def __init__(self, session_id):
        self.email_id = 0
        self.email_dict = {}
        self.init = False # todo
        self.project_id = PROJECT_ID
        self.session_id = session_id
        self.language_code = "en-US"

        # build session
        self._build_session()


    def _build_session(self):
        self.session_client = dialogflow.SessionsClient.from_service_account_json(
            './test-conv-ai-1011-3b1d693b53da.json')  # todo: need a more reasonable way to hardcode the file path

        self.session = self.session_client.session_path(self.project_id, self.session_id)
        print("Session path: {}\n".format(self.session))


    def parse_command_dialogflow(self, text):
        action, args, fulfill_text = self._detect_intent_texts(text)
        self._parse_args(action, args, fulfill_text)

        return action, self.email_id, args, fulfill_text


    def _detect_intent_texts(self, text):
        text_input = dialogflow.TextInput(text=text, language_code=self.language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = self.session_client.detect_intent(
            request={"session": self.session, "query_input": query_input}
        )

        # intent = response.query_result.intent.displayName
        action = response.query_result.action  # string
        args = response.query_result.parameters  # dict
        fulfill_text = response.query_result.fulfillment_text  # string, this is the response text

        return action, args, fulfill_text


    def _parse_args(self, action, args, fulfill_text):
        if action.split('.')[0] == "command":  # means this is an operation to the email, e.g. forward, delete, mark as read
            if dict_is_empty(args):  # no reference words (such as "this", "today") are gained todo: maybe we will also have other kinds of parameters, such as the email addr to forward to
                fulfill_text = "Can you say that again?"
                # do not modify email_id in this case
            else:
                query = ""
                self._query_backend_and_update(query)

        return action, args, fulfill_text


    def _query_backend_and_update(self, query):
        # todo: send query info to backend
        commmand = "search" # in this case, command must be "search"
        email_id = 0  # initial email id, useless for searching
        args = {"query":query}
        response = _send_command(commmand, email_id, args) # dict

        # get email id and email content
        self.email_id = response["id"]
        self.email_dict = response


def _send_command(command, email_id, args):
    command_dict = {
        "command": command,
        "id": email_id,
        "args": args
    }
    response = requests.get(
        f"http://localhost:{nlp.app.config['BACKEND_SERVER_PORT']}/api/command/", json=command_dict)
    # print(response)
    data = response.json()
    # print(data)
    return data["response"]


def dict_is_empty(d):
    for v in d.values():
        if v != '':
            return True
    return False