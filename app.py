__author__ = 'Ken and Narcisa'

from flask import Flask, jsonify, render_template, request, redirect
from random import choice
import argparse
import json
import pprint
import sys
import urllib
import requests
from urllib2 import urlopen
import re
import random

app = Flask(__name__)
app.config["DEBUG"] = False  # Only include this while you are testing your app

sampleText = "Hey what are you doing tonight?"

def splitText(text):
	return text.split()

def scrapeRhymeZone():
	words = splitText(sampleText.replace("?",""))
	baseURL = "http://www.rhymezone.com/r/rhyme.cgi?Word="
	endURL = "&org1=syl&org2=l&org3=y&typeofrhyme=perfect"
	finalString = ""
	for i in words:
		soup = BeautifulSoup(urlopen(baseURL + i + endURL))
		soup.select(".d~ a")
		soup.select(".d")
		rhymingWords = soup.select("font b a")
		finalRhymingWords = []
		for i in rhymingWords:
			result = re.sub(str("<.*?>"), str(""), str(i))
			result = result.replace("\xc2\xa0", " ")
			if not " " in result:
				finalRhymingWords.append(result)	
		finalString += finalRhymingWords[random.randint(0,len(finalRhymingWords)-1)] + " "
	print(finalString)

scrapeRhymeZone()

#.d~ a , .d , font b a

@app.route("/")
def home():
#return "Hello World"
	return render_template('hello.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
