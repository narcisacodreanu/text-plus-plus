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
from bs4 import BeautifulSoup
import nltk
from nltk import word_tokenize,pos_tag 
from twilio.rest import TwilioRestClient

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
		for i in range(len(rhymingWords)):
			result = re.sub(str("<.*?>"), str(""), str(rhymingWords[i]))
			result = result.replace("\xc2\xa0", " ")
			if not " " in result:
				finalRhymingWords.append(result)	
		finalString += finalRhymingWords[random.randint(0,len(finalRhymingWords)-1)] + " "
	return finalString

def sendText(text, mediaURL):
	ACCOUNT_SID = "AC591d7f09e4a2c9c028c89d4f40488f49" 
	AUTH_TOKEN = "68c447907fe59e086289a9c914ccce47"
	client =  TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
	client.messages.create(
			to="5169966173", 
			from_="+15168743771",
			body=text,
			media_url=mediaURL
	)
	return "sent"

print(scrapeRhymeZone())

def gifUrlGenerator(noun):
	data = json.loads(urllib.urlopen("http://api.giphy.com/v1/gifs/search?q="+ noun + "&api_key=dc6zaTOxFJmzC&limit=5").read())
	#gif_response = json.dumps(data, sort_keys=True, indent=4)
	gif_url = data["data"][0]["images"]["fixed_height"]["url"]
	return gif_url

def getNoun(sampleText):
	text = word_tokenize(sampleText)
	array = nltk.pos_tag(text)
	t = tuple(i[1] for i in array)
	noun = "funny"
	for i in array:
		if i[1] == "NN":
			noun = i[0]
	return noun
	
print gifUrlGenerator(getNoun(sampleText))
#.d~ a , .d , font b a

@app.route("/")
def home():
#return "Hello World"
	return render_template('hello.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
