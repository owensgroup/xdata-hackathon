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

#wordhist = sorted([wordhist(v,k),for (k,v) in wordhist.items()], reverse = True)

if __name__ == "__main__":
	data_dir = gd.GetDataDirList()
	tweets = gd.GetJsonObj(data_dir[0]+'yemen_tweets_5.22.2016')
	tweetstr, _ = gd.GenerateTweetString(tweets)
	#stemstr = stemm(tweetstr)
	
	wordhist = tokenize(tweetstr)
	wordhist = sorted([(k,v) for (v,k) in wordhist.items()], reverse = True) 
	
	
	for i in range(1,100):
		print(wordhist[i])








	
