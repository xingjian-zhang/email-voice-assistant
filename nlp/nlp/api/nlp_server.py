import flask
from flask import json, request
import nlp

@nlp.app.route('/', methods=["GET"])
def index():
    return "helloworld"