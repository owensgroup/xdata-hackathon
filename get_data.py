#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pylab

data_dir=[]
with open('data.conf', 'rb') as f:
    data_dir = f.read().splitlines()

tweet_file = data_dir[0]

tweets = []
count = 0
for line in open(tweet_file, 'r'):
    tweets.append(json.loads(line))
    count = count + 1
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
        coo = item['_source']['doc']['place']['bounding_box']['coordinates'][0]
        fig1 = plt.figure(1)
    	ax1 = fig1.add_subplot(111, aspect='equal')
    	#print coo
	width = coo[2][0]-coo[0][0]
	height = coo[2][1]-coo[0][1]
	#print width
	ax1.add_patch(
    		patches.Rectangle(
       		(coo[0][0], coo[0][1]),   # (x,y)
       		width,          # width
       		height,          # height
   		fill = False
		)
    	)
    	pylab.ylim([10,30]);
    	pylab.xlim([10,30]);
plt.show()

fig1.savefig('rect1.png', dpi=90, bbox_inches='tight')
    

