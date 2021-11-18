from google.cloud import dialogflow
import nlp
import requests

PROJECT_ID = "test-conv-ai-1011"
LANGUAGE_CODE = "en-US"

class Dialogflow_session:
    def __init__(self, session_id):
        self.email_id = 0
        self.email_dict = {}
        # self.init = False # todo
        self.project_id = PROJECT_ID
        self.session_id = session_id
        self.language_code = LANGUAGE_CODE

        # build session
        self._build_session()


    def _build_session(self):
        self.session_client = dialogflow.SessionsClient.from_service_account_json(
            './test-conv-ai-1011-3b1d693b53da.json')  # todo: need a more reasonable way to hardcode the file path

        self.session = self.session_client.session_path(self.project_id, self.session_id)
        print("Session path: {}\n".format(self.session))


    def parse_command_dialogflow(self, text):
        action, parameters, fulfill_text = self._detect_intent_texts(text)
        args = self._parse(action, parameters)

        return action, self.email_id, args, fulfill_text


    def _detect_intent_texts(self, text):
        text_input = dialogflow.TextInput(text=text, language_code=self.language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = self.session_client.detect_intent(
            request={"session": self.session, "query_input": query_input}
        )

        # intent = response.query_result.intent.displayName
        action = response.query_result.action  # string
        parameters = response.query_result.parameters  # dict
        fulfill_text = response.query_result.fulfillment_text  # string, this is the response text

        return action, parameters, fulfill_text


    def _parse(self, action, parameters):
        """
        modify: self.email_id, self.email_dict
        return: args for sending command
        """
        if action.split('.')[0] == "command":  # means this is an operation to the email, e.g. forward, delete, mark as read
            mode = action.split('.')[2]
            if mode == "this": # manipulate on current email
                pass
            elif mode == "time":
                date = parameters["date-time"][:len("0000-00-00")]
                query = f"after:{date} before:{date}" # exactly this day
                self._query_backend_and_get_email(query)
            elif mode == "confirm":
                pass
            else:
                raise Exception(f"mode [{mode}] is not implemented")

        elif action.split('.')[0] == "dialog": # means this is only a normal dialog, no action needed
            pass # todo

        args = {} # todo
        return args


    def _query_backend_and_get_email(self, query):
        commmand = "search" # in this case, command must be "search"
        email_id = 0  # useless, only a placeholder
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