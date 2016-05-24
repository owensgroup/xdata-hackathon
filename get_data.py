#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import cPickle
import os.path
import gzip

def ExtractTime(json):
    try:
        timestamp = int(json['_source']['doc']['timestamp_ms'])
        center_x = json['_source']['doc']['bbox_center_x']
        center_y = json['_source']['doc']['bbox_center_y']
        return (timestamp, center_x, center_y)
    except KeyError:
        return 0

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
    #i = 0
    for line in open(tweet_file, 'r'):
        #i += 1
        tweets.append(json.loads(line))
        #if i > 10000:
        #    break
    return tweets

def GenerateTweetString(tweets):
    sorted_tweets = []
    #keys = aggression, urgent, peace, saudi arabia, yemeni (people of yemen), houthi, alliance, rocket, yemen, crisis, sanna, taiz, aden, missile, news
    keys = [u'العدوان', u'عاجل', u'امن', u'السعودية', u'اليمنية', u'الحوثي',u'التحالف',u'صاروخ',u'ﺎﻠﻴﻤﻧ', u'ﺃﺰﻣﺓ', u'ﺺﻨﻋﺍﺀ', u'ﺖﻋﺯ', u'ﻉﺪﻧ', u'ﺹﺍﺭﻮﺧ', u'ﺄﺨﺑﺍﺭ']
    jsonstr = []
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
            jsonstr.append(text)
            sorted_tweets.append(item)
            if item['_source']['doc']['place'] != None and item['_source']['doc']['place']['bounding_box'] != None and item['_source']['doc']['place']['bounding_box']['coordinates'] != None:
                topleft_x = float(item['_source']['doc']['place']['bounding_box']['coordinates'][0][0][0])
                topleft_y = float(item['_source']['doc']['place']['bounding_box']['coordinates'][0][0][1])
                bottomright_x = float(item['_source']['doc']['place']['bounding_box']['coordinates'][0][2][0])
                bottomright_y = float(item['_source']['doc']['place']['bounding_box']['coordinates'][0][2][1])
                center_x = int((bottomright_x-topleft_x)/2)
                center_y = int((bottomright_y-topleft_y)/2)
                item['_source']['doc']['bbox_center_x'] = center_x
                item['_source']['doc']['bbox_center_y'] = center_y
            item['_source']['doc']['bbox_center_x'] = 0
            item['_source']['doc']['bbox_center_y'] = 0
    return jsonstr,sorted_tweets

def main():
    data_dir = GetDataDirList()
    tweets = GetJsonObj(data_dir[0]+'yemen_tweets_5.22.2016')
    tweetstr,sorted_tweets = GenerateTweetString(tweets)
    sorted_tweets.sort(key=ExtractTime)

if __name__ == "__main__":
    main()




