# -*- coding:utf-8 -*-
from urllib import quote_plus
from search.util.config_read_util import *

# 代理
PROXY = 'kb111.asuscomm.com:8118'
# 要搜索的内容
# KEYWORDS = '@spam since:2018-10-01 until:2018-11-01'

# 推特用户数据库
# userHost = 'mongodb://kb314:fzdwxxcl.314@121.49.99.14:30011'
userHost = "mongodb://%s:%s@%s" % (quote_plus('readAnyDatabase'), quote_plus('Fzdwxxcl.121'), '121.49.99.14:30011')
userDatabase = 'Account'
userCollection = 'TwitterAccount2019'

# 推特用户信息存储数据库
# tweet_host = "mongodb://%s:%s@%s" % ('hepengtao', 'hepengtao319', '121.49.99.14:30011')
tweet_host = "mongodb://127.0.0.1:27017"
tweet_database = "twitter_user_tweet"
tweet_collection = "user"
