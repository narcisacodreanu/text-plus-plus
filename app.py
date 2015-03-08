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
app.config["DEBUG"] = True  # Only include this while you are testing your app

sampleText = "Today I went to the zoo!"

def splitText(text):
	return text.split()

def scrapeRhymeZone(text):
	punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
	no_punct = ""
	punctuation = []
	words = splitText(text)
	for i in range(len(words)):
		newWord = ""
		for j in words[i]:
			if j not in punctuations:
				newWord = newWord + j
			else:
				punctuation.append((j,i))
		i = newWord
			
	baseURL = "http://www.rhymezone.com/r/rhyme.cgi?Word="
	endURL = "&org1=syl&org2=l&org3=y&typeofrhyme=perfect"
	finalString = ""
	finalWords = []
	for i in words:
		soup = BeautifulSoup(urlopen(baseURL + i + endURL))
		soup.select(".d~ a")
		soup.select(".d")
		rhymingWords = soup.select("font b a")
		finalRhymingWords = []
		if len(rhymingWords) > 0:
			for i in range(len(rhymingWords)):
				result = re.sub(str("<.*?>"), str(""), str(rhymingWords[i]))
				result = result.replace("\xc2\xa0", " ")
				if not " " in result:
					finalRhymingWords.append(result)	
			finalWords.append(finalRhymingWords[random.randint(0,len(finalRhymingWords)-1)])
		else:
			finalWords.append(i)
	for i in range(len(finalWords)):
		finalString += finalWords[i]
		for j in punctuation:
			if j[1] == i:
				finalString+=j[0]
		if i != len(finalWords) - 1:
			finalString += " "
	print(finalWords)
	return finalString


def sendText(text, mediaURL, phone_number):
	ACCOUNT_SID = "AC591d7f09e4a2c9c028c89d4f40488f49" 
	AUTH_TOKEN = "68c447907fe59e086289a9c914ccce47"
	client =  TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
	client.messages.create(
			to="+" + phone_number, 
			from_="+15168743771",
			body=text,
			media_url=mediaURL
	)
	return "sent"

def gifUrlGenerator(noun):
	data = json.loads(urllib.urlopen("http://api.giphy.com/v1/gifs/search?q="+ noun + "&api_key=dc6zaTOxFJmzC&limit=5").read())
	#gif_response = json.dumps(data, sort_keys=True, indent=4)
	appropriate = False
	print(data["data"][0]["rating"])
	while not appropriate:
		if len(data["data"]) > 20:
			randomNumber = random.randint(0,20)
		else:
			randomNumber = random.randint(0, len(data["data"])-1)
		if data["data"][randomNumber]["rating"] is "r":
			appropriate = False
		else:
			appropriate = True
	gif_url = data["data"][randomNumber]["images"]["fixed_height"]["url"]
	return gif_url

def getNoun(sampleText):
	text = word_tokenize(sampleText)
	array = nltk.pos_tag(text)
	t = tuple(i[1] for i in array)
	noun = "funny"
	for i in array:
		if "NN" in i[1]:
			noun = i[0]
	return noun
	
print gifUrlGenerator(getNoun(sampleText))

#.d~ a , .d , font b a

@app.route("/")
def home():
#return "Hello World"
	return render_template('hello.html')

@app.route("/done", methods=["GET", "POST"])
def text():
	if request.method == "POST":
		print("here")
		phone_number = request.form["user_search"]
		text = request.form["text"]
		rhymedText = scrapeRhymeZone(text)
		gif_URL = gifUrlGenerator(getNoun(text))
		sendText(rhymedText,gif_URL, phone_number)
		print(getNoun(text))
		return render_template("done.html", originalText=text,rhymedText=rhymedText, gif=gif_URL, phone=phone_number)
	else:
		return render_template("done.html")
	return render_template("done.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0")
