import json
import flask
import nlp
from flask import request, session
import requests
import os
import sys
from pathlib import Path
from tkinter import *
from google.cloud import dialogflow
import datetime
import random
from .summarize import Summarize

LOGGING = False
if LOGGING:
    fp = open('log.txt', 'w')

# for dialogflow
PROJECT_ID = "test-conv-ai-1011"
LANGUAGE_CODE = "en-US"

OPERATIONS = ["read", "unread","delete","spam","forward"]

summarizer = Summarize()

@nlp.app.before_first_request
def init_dialogflow():
    # if not session.get("df_id"):
    session_id = 1234
    session["df_id"] = session_id # store the df session_id in flask session object
    nlp.df_sessions[session_id] = Dialogflow_session(session_id=session_id)
    with open('log_2.txt', 'w') as f:
        f.write("Diagflow Initialized")


@nlp.app.route('/', methods=["GET"])
def base():
    return "Welcome to the NLP server!"


# @nlp.app.route('/voice/', methods=["POST"])
# def parse_voice():
#     # 1. save voice
#     voice_file = request.files["voice"]
#     # voice_file.save("test.mp3")
#     # sound = AudioSegment.from_mp3("test.mp3")
#     # sound.export("test.wav", format="wav")

#     # 2. speech2text
#     user_text = _speech_to_text(voice_file)
#     # TODO: Ambiguity Regex Match!
#     user_text = user_text.replace("*", "star")  # FIX ME!!!
#     user_text = user_text.replace("start", "star")
#     user_text = user_text.replace("fire", "star")
#     user_text = user_text.replace("stop", "star")
#     if LOGGING:
#         fp.write("User: "+user_text+"\n")

#     # 3. parse command, email_id & args
#     command = _parse_command(user_text)
#     # text = "Receive your command: " + command
#     # fp.write(text+"\n")

#     email_id = 0
#     args = {}

#     # 4. send command to backend
#     if command != "default":
#         response = _send_command(command, email_id, args)

#     # 5. generate response = generated by AI
#     # print('response generate')
#     if command == "default":
#         bot_text = "Sorry, can you speak again?"
#     elif command == "reply":
#         pass
#     elif command == "show":
#         bot_text = _mail_dict_to_str(response)
#         bot_text += "\n--------------------\nWhat can I do for you?"
#         bot_text = "SHOW"+bot_text
#     else:
#         bot_text = "OK."
#     # # 6. text2speech
#     # _text_to_audio(bot_text, "test_output.mp3")

#     if LOGGING:
#         fp.write(bot_text+"\n")

#     return flask.jsonify({
#         "user": user_text,
#         "bot": bot_text
#     })


@nlp.app.route('/response/', methods=["GET"])
def get_response():
    user_text = request.args.get('text')
    if LOGGING:
        fp.write("User: "+user_text+"\n")

    # command, email_id, args = _parse_command(user_text)
    # # 3. parse command, email_id & args
    # # text = "Receive your command: " + command
    # # fp.write(text+"\n")
    #
    # email_id = 0
    # args = {}
    #
    # # 4. send command to backend
    # if command != "default":
    #     response = _send_command(command, email_id, args)
    #
    # # 5. generate response = generated by AI
    # # print('response generate')
    # if command == "default":
    #     bot_text = "Sorry, can you speak again?"
    # elif command == "reply":
    #     pass
    # elif command == "show":
    #     bot_text = _mail_dict_to_str(response)
    #     bot_text += "\n--------------------\nWhat can I do for you?"
    #     bot_text = "SHOW"+bot_text
    # else:
    #     bot_text = "OK."
    # # # 6. text2speech
    # # _text_to_audio(bot_text, "test_output.mp3")

    bot_response_dict = {
        "bot_text_start": None, # the response should start with this string
        "from": None, # sender name without email addr, e.g. Changyuan Qiu
        "to": None,  # recipient name without email addr, e.g. Changyuan Qiu
        "subject": None, # title
        "time": None, # send time
        "summary": None, # summary of the email
        "body": None, # whole body of the email
        "bot_text_end": None, # the response should end with this string, e.g. Do you want to know more about this email?
    }
    session_id = 1234
    df_session = nlp.df_sessions[session_id]
    action, email_ids, args, bot_text = df_session.parse_command_dialogflow(user_text)

    bot_response_dict["bot_text_start"] = bot_text
    action_type = action.split('.')[0]
    command = action.split('.')[1]  # e.g. read, unread, spam...

    # send command to backend only when the action is a "command" type and command is in OPERATIONS (operations on an email)
    if action_type == "command":
        if command in OPERATIONS: # send command to backend only when command is in OPERATIONS (operations on an email)
            for email_id in email_ids:
                _send_command(command, email_id, args)

        elif command == "speak_summary": # read the email out for the user
            sender_name = _get_name_from_sender(df_session.curr_email_dict["from"])
            recipient_name = _get_name_from_sender(df_session.curr_email_dict["to"])
            subject = df_session.curr_email_dict["subject"]
            time = df_session.curr_email_dict["time"]
            email_body = df_session.curr_email_dict["body"]

            meta = {'title':subject, 'author':sender_name}
            summary = summarizer.summarize(email_body, meta=meta) # todo: set the summary args

            bot_response_dict["from"] = sender_name
            bot_response_dict["to"] = recipient_name
            bot_response_dict["subject"] = subject
            bot_response_dict["time"] = time
            bot_response_dict["summary"] = summary
            bot_response_dict["bot_text_end"] = " Do you want to know more about this email?"

        elif command == "speak_whole": # read the email out for the user
            sender_name = _get_name_from_sender(df_session.curr_email_dict["from"])
            recipient_name = _get_name_from_sender(df_session.curr_email_dict["to"])
            subject = df_session.curr_email_dict["subject"]
            time = df_session.curr_email_dict["time"]
            email_body = df_session.curr_email_dict["body"]
            bot_response_dict["from"] = sender_name
            bot_response_dict["to"] = recipient_name
            bot_response_dict["subject"] = subject
            bot_response_dict["time"] = time
            bot_response_dict["body"] = email_body

    if LOGGING:
        fp.write(bot_text+"\n") # todo: how to log properly? bot text is not a complete response

    return flask.jsonify({
        "user": user_text,
        "bot": bot_response_dict
    })


def _get_name_from_sender(sender:str) -> str:
    email_addr_start_idx = sender.find('<')
    name = sender[:email_addr_start_idx]
    return name.strip()


def _mail_dict_to_str(mail_dict):
    """
    >>> mail_dict = {
            "id": email_id,
            "from": message.sender,
            "to": message.recipient.split(","),
            "subject": message.subject,
            "time": message.timestamp,
            "body": message.body
        }
    """
    _to_print = []
    _to_print.append("{:10s}: {}".format("Subject", mail_dict["subject"]))
    _to_print.append("{:10s}: {}".format("From", mail_dict["from"]))
    _to_print.append("{:10s}: {}".format("To", ";".join(mail_dict["to"])))
    _to_print.append("{:10s}: {}".format("Time", mail_dict["time"]))
    _to_print.append("{:10s}: \n{}".format("Body", mail_dict["body"]))
    return "\n".join(_to_print)


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


# def _speech_to_text(path, verbose=False):
#     '''
#     path:       the path to the speech file
#     returns:    text version of speech content
#     '''
#     r = sr.Recognizer()
#     text = ""
#     with sr.AudioFile(path) as source:
#         audio_text = r.listen(source)
#         text = ""
#         try:
#             text = r.recognize_google(audio_text)
#             if verbose:
#                 print('Converting audio transcripts into text ...')
#                 print(text)
#         except:
#             print('Sorry.. run again...')
#     return text


def _parse_command(text, keywords=Path(nlp.__file__).parent / "command_keywords.txt"):
    '''
    text:       the text to be parsed for commands
    keywords:   either a set of string, or a path to keywords_file
    returns:    query dict containing counts of each keyword
    '''
    # email_dict = _get_email(email_id)  # for other functionalities

    # 1. get keywords first
    if isinstance(keywords, set):
        keywords = keywords
    else:
        try:
            keywords_file = open(keywords, 'r+')
            keywords = set(line.rstrip() for line in keywords_file.readlines())
        except FileNotFoundError:
            print("Keywords file not found")

    def preprocess(word: str) -> str:
        return word.lower()  # FIXME:

    query = dict()
    for word in text.split(' '):
        word = preprocess(word)
        if word in keywords:
            query[word] = query.get(word, 0) + 1

    command = "default"
    max_count = -1
    for keyword, count in query.items():
        if count > max_count:
            command = keyword

    if command == "*":
        command = "star"  # FIXME:

    # 2. get email_id and other args
    email_id = 0
    args = {}

    return command, email_id, args


# def _text_to_audio(text: str, save_file, language="en", slow=False):
#     OUTPUT_DIR = Path(nlp.__file__).parent / "output_audio"
#     audio_obj = gTTS(text=text, lang=language, slow=slow)

#     ext = os.path.splitext(save_file)[-1]
#     if ext.lower() == ".mp3":
#         audio_obj.save(str(OUTPUT_DIR / save_file))
#     elif ext.lower() == ".wav":
#         audio_obj.save(str(OUTPUT_DIR / "tmp.mp3"))
#         sound = AudioSegment.from_mp3(str(OUTPUT_DIR / "tmp.mp3"))
#         sound.export(str(OUTPUT_DIR / save_file), format="wav")
#     else:
#         print("Unsupported format, available formats are mp3 and wav", file=sys.stderr)
#         raise NotImplementedError


class Dialogflow_session:
    def __init__(self, session_id):
        self.curr_email_id = "" # id of curr email
        self.curr_email_dict = {} # dict of curr email
        self.query_email_ids = [] # list of id from query
        self.query_email_dicts = [] # list of dicts from query
        self.project_id = PROJECT_ID
        self.session_id = session_id
        self.language_code = LANGUAGE_CODE

        # build session
        self._build_session()

        # get email id of the latest email
        self._init_curr_email()


    def _build_session(self):
        self.session_client = dialogflow.SessionsClient.from_service_account_json(
            str(Path("/Users/hangruicao/Documents/eecs498/email-voice-assistant/nlp/nlp/") / "dialogflow" / "private_key"/ "test-conv-ai-1011-3b1d693b53da.json"))  # todo: need a more reasonable way to hardcode the file path

        self.session = self.session_client.session_path(self.project_id, self.session_id)
        print("Session path: {}\n".format(self.session))


    def _init_curr_email(self):
        commmand = "latest"  # in this case, command must be "latest"
        email_id = 0  # useless, only a placeholder
        args = {}
        response = _send_command(commmand, email_id, args)  # list of dicts
        if len(response) > 1:
            raise Exception("There should be only one latest email. Check if somethind went wrong.")
        self.curr_email_id = response[0]["id"]
        self.curr_email_dict = response[0]


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
        return: args for sending command, and a list of email ids
        """
        email_ids = [self.curr_email_id]
        action_type = action.split('.')[0]

        if action_type == "command":  # means this is an operation to the email, e.g. forward, delete, mark as read
            mode = action.split('.')[2]
            if mode == "ref": # ref to this/next/prev email
                ref_word = parameters.get("referencewords")
                if ref_word is not None:
                    if ref_word == "this email":
                        pass
                    elif ref_word == "next email":
                        self._get_next_or_prev_email("next")
                        email_ids = [self.curr_email_id]
                    elif ref_word == "previous email":
                        self._get_next_or_prev_email("prev")
                        email_ids = [self.curr_email_id]
                    else:
                        raise ValueError(f"invalid ref word: {ref_word}")

            elif mode == "time":
                date = parameters["date-time"][:len("0000-00-00")]
                date_split = date.split('-')
                date = datetime.date(int(date_split[0]), int(date_split[1]), int(date_split[2]))
                prev_day = date - datetime.timedelta(days=1)
                next_day = date + datetime.timedelta(days=1)
                query = f"label:INBOX after:{prev_day.isoformat()} before:{next_day.isoformat()}" # query exactly this day
                self._query_backend_and_get_email(query) # modify self.email_id
                email_ids = self.query_email_ids

            elif mode == "followup_this": # followup on the current email, e.g. Do you want to know more about this email? - Yes.
                pass
            elif mode == "no_action":
                pass
            else:
                raise Exception(f"mode [{mode}] is not implemented")

        elif action_type == "dialog": # means this is only a normal dialog, no action needed
            pass # todo

        args = {} # todo: args sent to backend, sometimes should be a list (e.g. forward)
        return args, email_ids


    def _query_backend_and_get_email(self, query):
        commmand = "search" # in this case, command must be "search"
        email_id = 0  # useless, only a placeholder
        args = {"query":query}
        response = _send_command(commmand, email_id, args) # list of dicts
        # print(response)

        # get email id and email content
        self.query_email_ids = [email_dict["id"] for email_dict in response] # list of id
        self.query_email_dicts = response # list of dicts

    def _get_next_or_prev_email(self, command):
        assert command == "prev" or command == "next"
        email_id = self.curr_email_id
        args = {}
        response = _send_command(command, email_id, args)  # list of dicts
        if len(response) > 1:
            raise Exception("There should be only one email. Check if somethind went wrong.")
        self.curr_email_id = response[0]["id"]
        self.curr_email_dict = response[0]