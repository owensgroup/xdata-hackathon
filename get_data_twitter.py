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
count = 0
for item in tweets:
    #text = item['_source']['norm']['body']
    try:
        cc = item['_source']['doc']['coordinates']['coordinates']
    except TypeError:
        continue
    #flag = False
    #if cc == 'YE' or cc=='YEM':
    #    count+=1
    #    flag = True
    #for key in keys:
    #    if key in text:
    #        flag = True
    #        break
    #if flag:
    #author = item['_source']['norm']['author']
    #tweetid = item['_source']['doc']['id_str']
    #urls.append("https://twitter.com/"+author+"/status/"+tweetid)
    #if sort_data.extract_time(item) == 0:
    #    continue
    #if flag:
    sorted_tweets.append(item)

print count
#for url in urls:
#    print url

#sorted_tweets.sort(key=sort_data.extract_time)

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.basemap import Basemap

# Lambert Conformal Conic map.
fig1 = plt.figure()
themap = Basemap(projection='gall',
              llcrnrlon = 35,              # lower-left corner longitude
              llcrnrlat = 10,               # lower-left corner latitude
              urcrnrlon = 60,               # upper-right corner longitude
              urcrnrlat = 25,               # upper-right corner latitude
              resolution = 'l',
              area_thresh = 100000.0,
              )

themap.drawcoastlines()
themap.drawcountries()
themap.fillcontinents(color = 'gainsboro')
themap.drawmapboundary(fill_color='steelblue')

urls = []

for line in sorted_tweets:
    coo = line['_source']['doc']['coordinates']['coordinates']
    #ax1 = fig1.add_subplot(111, aspect='equal')
    #width = coo[2][0]-coo[0][0]
    #height = coo[2][1]-coo[0][1]
    #print coo[0][0], coo[0][1], coo[2][0], coo[2][1], width, height
    #print line['_source']['doc']['place']['full_name']
    #print width
    x, y = themap(coo[0],coo[1])
    if( themap.is_land(x,y)==False ):
        if coo[1]<14.176933 and coo[1]>12.251857 and coo[0]<55.094123 and coo[1]>50.787483:
            print "*"
        print coo
        text = line['_source']['norm']['body']
        author = line['_source']['norm']['author']
        tweetid = line['_source']['doc']['id_str']
        urls.append("https://twitter.com/"+author+"/status/"+tweetid)
        print "https://twitter.com/"+author+"/status/"+tweetid
        themap.plot( x, y,
            'o',                    # marker shape
            color='Indigo',         # marker colour
            markersize=4            # marker size
            )

plt.show()
fig1.savefig('plot2.png', bbox_inches='tight')
    #print line

#for url in urls:
    #print url
