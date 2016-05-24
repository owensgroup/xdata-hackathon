#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sort_data

data_dir=[]
with open('data.conf', 'rb') as f:
    data_dir = f.read().splitlines()

tweet_file = data_dir[0]

tweets = []
sorted_tweets = []
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
	sorted_tweets.append(item)

for url in urls:
    print url

sorted_tweets.sort(key=sort_data.extract_time)

for line in sorted_tweets:
    print(line['_source']['doc']['timestamp_ms'], line['_source']['doc']['place']['bounding_box']['coordinates'][0][0][0],
          line['_source']['doc']['place']['bounding_box']['coordinates'][0][0][1])

