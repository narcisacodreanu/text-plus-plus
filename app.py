__author__ = 'Ken'
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import requests

app = Flask(__name__)
app.config["DEBUG"] = True  # Only include this while you are testing your app

def fun():
	as;ldjf

@app.route("/")
def home():
	return "Hello World"


if __name__ == '__main__':
    app.run(host="0.0.0.0")
