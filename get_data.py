#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import cPickle
import os.path
import gzip

def SavePickle(obj, fname, protocol = -1):
    file = gzip.GzipFile(fname, 'wb')
    cPickle.dump(obj, file, protocol)
    file.close()

def LoadPickle(fname):
    file = gzip.GzipFile(fname, 'rb')
    obj = cPickle.load(file)
    file.close()
    return obj

def GetDataDirList():
    data_dir=[]
    with open('data.conf', 'rb') as f:
        data_dir = f.read().splitlines()
    return data_dir

def GetJsonObj(tweet_file):
    tweets = []
    for line in open(tweet_file, 'r'):
        tweets.append(json.loads(line))
    return tweets

def GenerateTweetString(tweets):
    #yemen, crisis, sanna, taiz, aden, missile, news
    keys = [u'اليمن', u'أزمة', u'صنعاء', u'تعز', u'عدن', u'صاروخ', u'أخبار']
    jsonstr = ''
    for item in tweets:
        text = item['_source']['norm']['body']
        flag = False
        for key in keys:
            if key in text:
                flag = True
                break
        if flag:
            #author = item['_source']['norm']['author']
            #tweetid = item['_source']['doc']['id_str']
            #urls.append("https://twitter.com/"+author+"/status/"+tweetid)
            jsonstr += (text + ' ')
    return jsonstr

def main():
    data_dir = GetDataDirList()
    tweets = GetJsonObj(data_dir[0]+'yemen_tweets_5.22.2016')
    tweetstr = GenerateTweetString(tweets)

if __name__ == "__main__":
    main()




