#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

data_dir=[]
with open('data.conf', 'rb') as f:
    data_dir = f.read().splitlines()

tweet_file = data_dir[0]

tweets = []
for line in open(tweet_file, 'r'):
    tweets.append(json.loads(line))
    #print json.dumps(tweets[0], indent=4, sort_keys=True)
    #break
urls = []
#yemen, crisis, sanna, taiz, missile news
keys = [u'اليمن', u'أزمة', u'صنعاء', u'تعز', u'صاروخ', u'أخبار']
for item in tweets:
    text = item['_source']['norm']['body']
    flag = False
    for key in keys:
        if key in text:
            flag = True
            break
    if flag:
        author = item['_source']['norm']['author']
        tweetid = item['_source']['doc']['id_str']
        urls.append("https://twitter.com/"+author+"/status/"+tweetid)

for url in urls:
    print url



