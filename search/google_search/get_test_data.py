# -*- coding:utf-8 -*-
from pymongo import MongoClient
import json
import codecs
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


# the_host='mongodb://liuchang:liuchang314@121.49.99.14:30011'
def get_data(the_host='mongodb://127.0.0.1:27017',
             the_db='google',
             the_col='search_result'):
    """
    根据领英用户链接列表，从数据库中查找用户的详细信息
    :param the_host: 服务器地址
    :param the_db: 数据库
    :param the_col: 集合
    :param person_websites: 待查找的用户主链接列表
    :return: 查找的结果
    """

    data_col = MongoClient(the_host).get_database(the_db).get_collection(the_col)
    # search_fail = []    # 存放查找失败的用户
    # {"_id": 0, "person_website": 1, "name": 1, "title": 1, "head_url": 1,"company_location": 1, "background_summary": 1, "head_image": 1}
    user_detail = data_col.find()
    with codecs.open("google_data.txt", 'a', encoding='utf-8') as f:
        for user in user_detail:
            if user["webpage_url"] is None:
                webpage_url = "webpage_url:"
                f.write(webpage_url)
                f.write("\n")
            else:
                webpage_url = "webpage_url:" + user["webpage_url"]
                f.write(webpage_url)
                f.write("\n")
            if user["webpage_description"] is None:
                webpage_description = "webpage_description:"
                f.write(webpage_description)
                f.write("\n")
            else:
                webpage_description = "webpage_description:" + user["webpage_description"]
                f.write(webpage_description)
                f.write("\n")
            if user["webpage_title"] is None:
                webpage_title = "webpage_title:"
                f.write(webpage_title)
                f.write("\n")
            else:
                webpage_title = "webpage_title:" + user["webpage_title"]
                f.write(webpage_title)
                f.write("\n")
            f.write("\n")


if __name__ == "__main__":
    get_data()
