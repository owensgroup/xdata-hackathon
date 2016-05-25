#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import cPickle
import os.path
import gzip
from sets import Set

from os import listdir
from os.path import isfile, join

days_since = {'Jan2015':0, 'Feb2015':31, 'Mar2015':31, 'Apr2015':90, 'May2015':120, 'Jun2015':151, 'Jul2015':181, 'Aug2015':212, 'Sep2015':243, 'Oct2015':273, 'Nov2015':304, 'Dec2015':334, 'Jan2016':365, 'Feb2016':394, 'Mar2016':423, 'Apr2016':454, 'May2016':484}

def ReplaceRight(source, target, replacement, replacements=None):
    return replacement.join(source.rsplit(target, replacements))

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

def GetJsonObj(jsonfile):
    jsonobjs = []
    #i = 0
    for line in open(jsonfile, 'r'):
        #i += 1
        jsonobjs.append(json.loads(line))
        #print json.dumps(jsonobjs[-1], indent=4)
        #break
        #if i > 10000:
        #    break
    return jsonobjs

def GenerateTelegramString(teles):
    textstr = []
    titlestr = Set()
    count = 0
    for item in teles:
        if item['_source']['doc'] != None and 'text' in item['_source']['doc']:
            count += 1
            text = item['_source']['doc']['text']
            if 'sender' in item['_source']['doc']:
                title = item['_source']['doc']['sender']['title']
            elif 'from' in item['_source']['doc']:
                title = item['_source']['doc']['from']['title']
            textstr.append(text)
            titlestr.add(title)
    print count
    return textstr,titlestr

def GenerateTweetString2(tweets):
    sorted_tweets = []
    #keys = al-qaeda, aggression, urgent, peace, saudi arabia, yemeni (people of yemen), houthi, alliance, rocket, yemen, crisis, sanna, taiz, aden, missile, news
    keys = [u'القاعدة', u'العدوان', u'عاجل', u'امن', u'السعودية', u'اليمنية', u'الحوثي',u'التحالف',u'صاروخ',u'ﺎﻠﻴﻤﻧ', u'ﺃﺰﻣﺓ', u'ﺺﻨﻋﺍﺀ', u'ﺖﻋﺯ', u'ﻉﺪﻧ', u'ﺹﺍﺭﻮﺧ', u'ﺄﺨﺑﺍﺭ']
    jsonstr = []
    count = 0
    for item in tweets:
        #geo.coordinates
        #actor.preferredUsername
        if item['geo']!=None and 'coordinates' in item['geo']:
            count += 1
        text = item['body']
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
    print count
    return jsonstr,sorted_tweets
        
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
        #if( themap.is_land(x,y)==True ):
        themap.plot( x, y,
            'o',                    # marker shape
            color='Indigo',         # marker colour
            markersize=4            # marker size
            )

    plt.show()
    fig1.savefig('plot.png', bbox_inches='tight')

def PrintGeolist( geotweets ):
    for line in geotweets:
        #text = line['_source']['norm']['body']
        author = line['_source']['norm']['author']
        tweetid = line['_source']['doc']['id_str']
        print "https://twitter.com/"+author+"/status/"+tweetid
    #print text will cause UnicodeEncodeError: 'ascii' codec can't encode characters in position 1-4: ordinal not in range(128)
        #print text
        print line['_source']['doc']['coordinates']['coordinates']

def ProcessTweets(data_dir):
    tweets = GetJsonObj(data_dir)
    tweetstr,sorted_tweets = GenerateTweetString(tweets)
    sorted_tweets.sort(key=ExtractTime)
    geotweets=FilterGeoloc(sorted_tweets)
    PlotTwitter(geotweets)
    PrintGeolist(geotweets)
    halfday = 43200000
    halfcity = 0.005 #sqrt(2.1km)/2
    edges_time, edges_distance = GenerateEdgeList(sorted_tweets, halfday, halfcity)
    #print len(edges_time), len(edges_distance)

def ExtractTweets(datadir):
    count = 0
    without_coord = 0
    tweets = []
    fnames = [f for f in listdir(datadir) if isfile(join(datadir,f)) and f[-1] == 'n']
    for fname in fnames:
        fullname =  datadir + fname
        #process json file
        with open(fullname) as user_tweets:
            jsonstr = ReplaceRight(user_tweets.read(), ',', '', 1)
            d = json.loads(jsonstr)
            for item in d['tweets']:
                time = item['created_at'].split()
                count += 1
                if item['coordinates'] == None:
                    without_coord += 1
                    continue
                if int(time[-1]) < 2015:
                    continue
                if days_since[time[1]+time[-1]]+int(time[2])<77:
                    continue
                tweets.append(item)
    print count, without_coord
    return tweets

def GetTuples(jsonobjs):
    tuples = []
    tweets = []
    idx = 0
    for item in jsonobjs:
        uname = item['user']['screen_name']
        tweet_id = item['id_str']
        x = float(item['coordinates']['coordinates'][0])
        y = float(item['coordinates']['coordinates'][1])
        time = item['created_at'].split()
        hms = time[3].split(':')
        t = days_since[time[1]+time[-1]]+int(time[2])*24*60+int(hms[0])*60+int(hms[1])
        tuples.append((idx, x, y, t))
        tweets.append((idx, int(tweet_id), uname))
    return tuples, tweets

def ProcessTeles(data_dir):
    teles = GetJsonObj(data_dir[0]+'yemen_telegram_5.22.2016')
    textstr,titlestr = GenerateTelegramString(teles)
    f = open('teles.txt', 'w')
    for item in textstr:
        f.write(item.encode("utf-8"))
        f.write('\n')
    f.close()

def main():
    more_tweets_dir = '/data/xdata-2016/more_tweets/'
    jsonobjs = ExtractTweets(more_tweets_dir)
    tuples,tweets = GetTuples(jsonobjs)
    print tuples[0]
    print tweets[0]
    print len(tuples)

if __name__ == "__main__":
    main()




