__author__ = 'Ken'
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request

from flask import Flask, jsonify, render_template, request, redirect
from random import choice
import argparse
import json
import pprint
import sys
import urllib
import urllib2

import requests
from bs4 import BeautifulSoup


app = Flask(__name__)
app.config["DEBUG"] = True  # Only include this while you are testing your app

sampleText = "Hey what are you doing tonight?"




@app.route("/")
def home():
	#return "Hello World"
	return render_template('hello.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
