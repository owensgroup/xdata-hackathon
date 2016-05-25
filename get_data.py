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
    #keys = al-qaeda, aggression, urgent, peace, saudi arabia, yemeni (people of yemen), houthi, alliance, rocket, yemen, crisis, sanna, taiz, aden, missile, news
    keys = [u'القاعدة', u'العدوان', u'عاجل', u'امن', u'السعودية', u'اليمنية', u'الحوثي',u'التحالف',u'صاروخ',u'ﺎﻠﻴﻤﻧ', u'ﺃﺰﻣﺓ', u'ﺺﻨﻋﺍﺀ', u'ﺖﻋﺯ', u'ﻉﺪﻧ', u'ﺹﺍﺭﻮﺧ', u'ﺄﺨﺑﺍﺭ']
    jsonstr = []
    for item in tweets:
        text = item['_source']['norm']['body']
        item['_source']['doc']['bbox_center_x'] = 0
        item['_source']['doc']['bbox_center_y'] = 0
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
    return jsonstr,sorted_tweets

def GenerateEdgeList(tweets, time_threshold, distance_threshold):
    edges_time = []
    edges_distance = []
    for i in range(len(tweets)-1):
        item = tweets[i]
        timestamp = int(item['_source']['doc']['timestamp_ms'])
        center_x = int(item['_source']['doc']['bbox_center_x'])
        center_y = int(item['_source']['doc']['bbox_center_y'])
        j = i + 1
        timestamp1 = int(tweets[j]['_source']['doc']['timestamp_ms'])
        while ((abs(timestamp1 - timestamp)) < time_threshold and j < len(tweets)):
            edges_time.append((i,j))
            edges_time.append((j,i))
            if (j+1 < len(tweets)):
                j += 1
            else:
                break
            timestamp1 = int(tweets[j]['_source']['doc']['timestamp_ms'])
        j = i + 1
        center_x1 = int(tweets[j]['_source']['doc']['bbox_center_x'])
        center_y1 = int(tweets[j]['_source']['doc']['bbox_center_y'])
        if (center_x1 == 0 and center_y1 == 0):
            continue
        distance = abs(center_x1*center_x1 - center_x*center_x)+abs(center_y1*center_y1-center_y*center_y)
        while (distance < distance_threshold and j < len(tweets)):
            edges_time.append((i,j))
            edges_time.append((j,i))
            if (j+1 < len(tweets)):
                j += 1
            else:
                break
            center_x1 = int(tweets[j]['_source']['doc']['bbox_center_x'])
            center_y1 = int(tweets[j]['_source']['doc']['bbox_center_y'])
    return edges_time, edges_distance

def FilterGeoloc(sorted_tweets):
    geotweets=[]
    for item in sorted_tweets:
        try:
            cc=item['_source']['doc']['coordinates']['coordinates']
        except TypeError:
            continue
        geotweets.append(item)
    return geotweets

def PlotTwitter(geotweets):
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

    for line in geotweets:
        coo = line['_source']['doc']['coordinates']['coordinates']
        #ax1 = fig1.add_subplot(111, aspect='equal')
        #width = coo[2][0]-coo[0][0]
        #height = coo[2][1]-coo[0][1]
        #print coo[0][0], coo[0][1], coo[2][0], coo[2][1], width, height
        #print line['_source']['doc']['place']['full_name']
        #print width
        x, y = themap(coo[0],coo[1])
        if( themap.is_land(x,y)==True ):
            themap.plot( x, y,
                'o',                    # marker shape
                color='Indigo',         # marker colour
                markersize=4            # marker size
                )

    plt.show()
    fig1.savefig('plot.png', bbox_inches='tight')

def main():
    data_dir = GetDataDirList()
    tweets = GetJsonObj(data_dir[0]+'yemen_tweets_5.22.2016')
    tweetstr,sorted_tweets = GenerateTweetString(tweets)
    sorted_tweets.sort(key=ExtractTime)
    geotweets=FilterGeoloc(sorted_tweets)
    PlotTwitter(geotweets)
    halfday = 43200000
    halfcity = 0.005 #sqrt(2.1km)/2
    edges_time, edges_distance = GenerateEdgeList(sorted_tweets, halfday, halfcity)
    #print len(edges_time), len(edges_distance)

if __name__ == "__main__":
    main()




