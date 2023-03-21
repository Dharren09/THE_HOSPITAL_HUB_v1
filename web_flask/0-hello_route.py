#!/usr/bin/python3
"""Starts the Flask Web  Application"""
from flask import Flask
app = Flask(__name__)



@app.route('/', strict_slashes=False)
def hello_thh():
    """Prints a message when / is called"""
    return 'Welcome to The Hospital Hub!, How can we be of help?'


if __name__=="__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5007)
