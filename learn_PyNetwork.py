#!/usr/bin/env python2.7.12
#coding=utf-8
#author="yexiaozhu"

import argparse
import json
import requests
import urllib2
import flickrapi
api_key = u'XXXXXX'
api_secret = u'XXXXXX'

try:
    from local_settings import flickr_apikey
except ImportError:
    pass

def collect_photo_info(api_key, tag, max_count):
    """Collects some interesting info about some photos from Flickr.com for a given tag"""
    photo_collection = []
    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')
    result_photo = flickr.photos.search(tags=tag)
    result_photo = json.loads(result_photo)
    count = 0
    for p in result_photo['photos']['photo']:
        if count >= max_count:
            return photo_collection
        print 'Processing photo: "%s"' %p['title']
        photo = {}
        info = flickr.photos.getInfo(photo_id=p['id'])
        info = json.loads(info)
        # url = "http://api.flickr.com/services/rest/?method=flickr.photos.getInfo&photo_id= " + p['id'] + "&format=json&nojsoncallback=1&api_key=" + api_key
        # info = requests.get(url).json()
        photo["flickrid"] = p['id']
        photo["title"] = info['photo']['title']['_content']
        photo["description"] = info['photo']['description']['_content']
        photo["page_url"] = info['photo']['urls']['url'][0]['_content']
        photo["farm"] = info['photo']['farm']
        photo["server"] = info['photo']['server']
        photo["secret"] = info['photo']['secret']

        # comments
        numcomments = int(json.loads(info['photo']['comments']['_content']))
        if numcomments:
            # print " Now reading comments (%d)..." % numcomments
            # url = "http://api.flickr.com/services/rest/?method=flickr.photos.comments.getList&photo_id=" + p['id'] + "&format=json&nojsoncallback=1&api_key=" + api_key
            # comments = requests.get(url).json()
            comments = flickr.photos.comments.getList(photo_id=p['id'])
            comments = json.loads(comments)
            photo["comment"] = []
            for c in comments['comments']['comment']:
                comment = {}
                comment["body"] = c['_content']
                comment["authorid"] = c['author']
                comment["authorname"] = c['authorname']
                photo["comment"].append(comment)
        photo_collection.append(photo)
        count = count + 1
    return photo_collection

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get photo info feom Flickr')
    parser.add_argument('--api-key', action="store", dest="api_key", default=flickr_apikey)
    parser.add_argument('--tag', action="store", dest="tag", default='sex')
    parser.add_argument('--max-count', action="store", dest="max_count", default=10, type=int)
    # parse arguments
    given_args = parser.parse_args()
    api_key, tag, max_count = given_args.api_key, given_args.tag, given_args.max_count
    photo_info = collect_photo_info(api_key, tag, max_count)
    for photo in photo_info:
        for k, v in photo.iteritems():
            if k == "title":
                print "Showiing photo info...."
            elif k == "comment":
                "\tPhoto got %s comments." % len(v)
            else:
                print "\t%s => %s" % (k, v)