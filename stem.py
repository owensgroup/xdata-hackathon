#!/usr/bin/env python
#comment
# -*- coding: utf-8 -*-
import json
import get_data as gd
import nltk
from nltk.stem.isri import ISRIStemmer

wordhist = {}

def stemm(tweetstr):
	stemmer = ISRIStemmer();
	stemstr = []
	for s in tweetstr:
		st = stemmer.stem(s)
		stemstr.append(st)
	return stemstr


def tokenize(stemstr):
	for s in stemstr:
		token = nltk.tokenize.wordpunct_tokenize(s)
		for t in token:
			if not wordhist.has_key(t):
				wordhist[t] = 1;
			else:
				wordhist[t] += 1;
	return wordhist

def tweetstemmer(historic):
	if historic==False:
		tweets = gd.GetJsonObj(data_dir[0]+'yemen_tweets_5.22.2016')
		tweetstr,_ = gd.GenerateTweetString(tweets)
	else:
		tweets = gd.GetJsonObj(data_dir[0]+'yemen_historic_tweets')
		tweetstr, _ = gd.GenerateTweetStringHistoric(tweets)
	return tweetstr

def telestemmer():
	teles = gd.GetJsonObj(data_dir[0]+'yemen_telegram_5.22.2016')
	textstr, _ = gd.GenerateTelegramString(teles)
	return textstr
	


if __name__ == "__main__":
	data_dir = gd.GetDataDirList()

	#process tweets
	historic = True
	#strlist = tweetstemmer(historic) 

	#process telegram text
	strlist = telestemmer()

	#stem using nlp
	#strlist = stemm(tweetstr) 
	
	#print(len(strlist))	

	wordhist = tokenize(strlist)
	wordhist = sorted([(k,v) for (v,k) in wordhist.items()], reverse = True) 
	
	#out = open("output_histweet500.txt", "w")
	#out = open("output_tweet500.txt", "w")
	out = open("output_telegram.txt", "w")
	
	for i in range(1,500):
		out.write(str(wordhist[i])+'\n')
	
	out.close()
	

	




	
