from google.cloud import dialogflow
import nlp
import requests
import datetime

PROJECT_ID = "test-conv-ai-1011"
LANGUAGE_CODE = "en-US"

class Dialogflow_session:
    def __init__(self, session_id):
        self.curr_email = 0
        self.email_id = 0 # id from query
        self.email_dict = {} # dict
        # self.init = False # todo
        self.project_id = PROJECT_ID
        self.session_id = session_id
        self.language_code = LANGUAGE_CODE

        # build session
        self._build_session()


    def _build_session(self):
        self.session_client = dialogflow.SessionsClient.from_service_account_json(
            '../token/test-conv-ai-1011-3b1d693b53da.json')  # todo: need a more reasonable way to hardcode the file path

        self.session = self.session_client.session_path(self.project_id, self.session_id)
        print("Session path: {}\n".format(self.session))


    def parse_command_dialogflow(self, text):
        # print("get user text")
        action, parameters, fulfill_text = self._detect_intent_texts(text)
        args, email_ids = self._parse(action, parameters)

        return action, email_ids, args, fulfill_text


    def _detect_intent_texts(self, text):
        text_input = dialogflow.TextInput(text=text, language_code=self.language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        # print("send query to df")

        response = self.session_client.detect_intent(
            request={"session": self.session, "query_input": query_input}
        )

        # print(response.query_result)
        action = response.query_result.action  # string
        parameters = response.query_result.parameters  # dict
        fulfill_text = response.query_result.fulfillment_text  # string, this is the response text

        return action, parameters, fulfill_text


    def _parse(self, action, parameters):
        """
        modify: self.email_id, self.email_dict
        return: args for sending command
        """
        email_ids = [self.curr_email]

        if action.split('.')[0] == "command":  # means this is an operation to the email, e.g. forward, delete, mark as read
            mode = action.split('.')[2]
            if mode == "this": # manipulate on current email
                pass
            elif mode == "time":
                date = parameters["date-time"][:len("0000-00-00")]
                date_split = date.split('-')
                date = datetime.date(int(date_split[0]), int(date_split[1]), int(date_split[2]))
                next_day = date + datetime.timedelta(days=1)
                query = f"after:{date.isoformat().replace('-','/')} before:{next_day.isoformat().replace('-','/')}" # query exactly this day
                # query = f"from:jimmyzxj@umich.edu" # query exactly this day
                self._query_backend_and_get_email(query) # modify self.email_id
                email_ids = [self.email_id]
            elif mode == "no_action":
                pass
            else:
                raise Exception(f"mode [{mode}] is not implemented")

        elif action.split('.')[0] == "dialog": # means this is only a normal dialog, no action needed
            pass # todo

        args = {} # todo: args sent to backend
        return args, email_ids


    def _query_backend_and_get_email(self, query):
        commmand = "search" # in this case, command must be "search"
        email_id = 0  # useless, only a placeholder
        args = {"query":query}
        response = _send_command(commmand, email_id, args) # dict
        print(response)

        # get email id and email content

        # self.email_ids = [email_dict["id"] for email_dict in response]
        self.email_id = response["id"] # single email
        self.email_dict = response


def _send_command(command, email_id, args):
    command_dict = {
        "command": command,
        "id": email_id,
        "args": args
    }
    response = requests.get(
        f"http://localhost:{3000}/api/command/", json=command_dict)
    # print(response)
    data = response.json()
    print(data)
    return data["response"]


def dict_is_empty(d):
    for v in d.values():
        if v != '':
            return True
    return False


df_session = Dialogflow_session(session_id=1234)
while True:
    user_text = input("Enter user text: ")
    # print("user text: ", user_text)
    if user_text == "quit":
        break
    action, email_ids, args, fulfill_text = df_session.parse_command_dialogflow(user_text)
    print("action: ", action)
    print("email ids: ", email_ids)
    print("args: ", args)
    print("bot text: ", fulfill_text)
    print('-'*20)

    if action.split('.')[1] == "mark_as_read" and action.split('.')[2] != "no_action":
        command = "read"
        for email_id in email_ids:
            _send_command(command, email_id, args)
    else:
        command = "default"


