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
		if not wordhist.has_key(token):
			wordhist[token] = 1;
		else:
			wordhist[token] += 1;
	return wordhist

#wordhist = sorted([wordhist(v,k),for (k,v) in wordhist.items()], reverse = True)

if __name__ == "__main__":
	data_dir = gd.GetDataDirList()
	tweets = gd.GetJsonObj(data_dir[0])
	tweetstr = gd.GenerateTweetString(tweets)
	stemstr = stemm(tweets)
	wordhist = tokenize(stemstr)
	wordhist = sorted([wordhist(v,k) for(k,v) in wordhist.items()], reverse = True) 
	
	keys = list(wordhist.keys())
	for i in range(1,10):
		print(keys[i])








	
