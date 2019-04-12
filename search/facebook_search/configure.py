# -*- coding:utf-8 -*-
from urllib import quote_plus

# 代理
PROXY = 'kb111.asuscomm.com:8118'
# 推特账户
account = 'hptuestc@gmail.com'
password = "He19910824_"

# 脸书用户数据库
# userHost = 'mongodb://kb314:fzdwxxcl.314@121.49.99.14:30011'
userHost = "mongodb://%s:%s@%s" % (quote_plus('readAnyDatabase'), quote_plus('Fzdwxxcl.121'), '121.49.99.14:30011')
userDatabase = 'Account'
userCollection = 'twitter'

# 脸书用户信息存储数据库
# facebook_host = "mongodb://%s:%s@%s" % ('', '', '121.49.99.14:30011')
facebook_host = "mongodb://127.0.0.1:27017"
facebook_database = "facebook"
facebook_collection = "user"
