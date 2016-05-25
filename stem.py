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
	textstr, _ = GenerateTelegramString(teles)
	return textstr
	


if __name__ == "__main__":
	data_dir = gd.GetDataDirList()
	#historic_tweets = GetJsonObj(data_dir[0]+'yemen_historic_tweets')
	#tweets = gd.GetJsonObj(data_dir[0]+'yemen_historic_tweets')
	#tweetstr, _ = gd.GenerateTweetString(tweets)
	#stemstr = stemm(tweetstr)
	
	#historic_tweets = GetJsonObj(data_dir[0]+'yemen_historic_tweets')
    	#tweetstr,sorted_tweets = GenerateTweetString2(historic_tweets)
	
	'''
	print(len(tweetstr))
	
	'''
	#process tweets
	historic = True
	strlist = tweetstemmer(historic) 

	#process telegram text
	#strlist = telestemmmer()

	#stem using nlp
	#strlist = stemm(tweetstr) 

	wordhist = tokenize(strlist)
	wordhist = sorted([(k,v) for (v,k) in wordhist.items()], reverse = True) 
	
	out = open("output_histweet500.txt", "w")
	
	for i in range(1,500):
		out.write(str(wordhist[i])+'\n')
	
	out.close()
	

	




	
