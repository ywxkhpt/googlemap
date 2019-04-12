# -*- coding:utf-8 -*-
from pymongo import MongoClient
import json
import codecs
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


# the_host='mongodb://liuchang:liuchang314@121.49.99.14:30011'
def get_data(the_host='mongodb://127.0.0.1:27017',
             the_db='twitter_user_tweet',
             the_col='user'):
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
    with codecs.open("twitter_data.txt", 'a', encoding='utf-8') as f:
        for user in user_detail:
            if user["name"] is None:
                name = "name:"
                f.write(name)
                f.write("\n")
            else:
                name = "name:" + user["name"]
                f.write(name)
                f.write("\n")
            if user["head_url"] is None:
                head_url = "head_url:"
                f.write(head_url)
                f.write("\n")
            else:
                head_url = "head_url:" + user["head_url"]
                f.write(head_url)
                f.write("\n")
            if user["person_website"] is None:
                person_website = "person_website:"
                f.write(person_website)
                f.write("\n")
            else:
                person_website = "person_website:" + user["person_website"]
                f.write(person_website)
                f.write("\n")
            if user["description"] is None:
                description = "description:"
                f.write(description)
                f.write("\n")
            else:
                description = "description:" + user["description"]
                f.write(description)
                f.write("\n")
            if user["head_image"] is None:
                head_image = "head_image:"
                f.write(head_image)
                f.write("\n")
            else:
                head_image = "head_image:" + user["head_image"]
                f.write(head_image)
                f.write("\n")
            if user["screen_name"] is None:
                screen_name = "screen_name:"
                f.write(screen_name)
                f.write("\n")
            else:
                screen_name = "screen_name:" + user["screen_name"]
                f.write(screen_name)
                f.write("\n")
            f.write("\n")


if __name__ == "__main__":
    get_data()
