#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from pymongo import MongoClient

# USER = config_read("database.ini", "mongodb", "USER")
# PASSWORD = config_read("database.ini", "mongodb", "PASSWORD")
# HOST = config_read("database.ini", "mongodb", "HOST")
# MONGODB = "mongodb://%s:%s@%s" % (USER, PASSWORD, HOST)
# db = MongoClient(MONGODB)
# database_linkedin_from = db[config_read("database.ini", "collection_linkedin", "database")]
# collection_linkedin_from = database_linkedin_from[
#     config_read("database.ini", "collection_linkedin", "collection")]

MONGODB_LOCAL = "mongodb://127.0.0.1:27017"
db_from = MongoClient(MONGODB_LOCAL)
database_linkedin_from = db_from["linkedin"]
collection_linkedin_from = database_linkedin_from["user_information"]

MONGODB_LOCAL = "mongodb://127.0.0.1:27017"
db_to = MongoClient(MONGODB_LOCAL)
database_linkedin_to = db_to["linkedin"]
collection_linkedin_to = database_linkedin_to["user_information_website"]

MONGODB_LOCAL = "mongodb://127.0.0.1:27017"
db_facebook = MongoClient(MONGODB_LOCAL)
database_linkedin_facebook = db_facebook["linkedin"]
collection_linkedin_facebook = database_linkedin_facebook["user_information_twitter_facebook"]


def filter():
    count = 0
    find = collection_linkedin_to.find()
    for item in find:
        for web in item['website']:
            url = str(web['url'])
            if 'facebook' in url:
                collection_linkedin_facebook.insert(item)
                print count
                count = count + 1
                break
    print "最终结果：", count


if __name__ == "__main__":
    filter()
