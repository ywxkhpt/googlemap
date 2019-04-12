# -*- coding:utf-8 -*-
from pymongo import MongoClient
import json

# the_host='mongodb://liuchang:liuchang314@121.49.99.14:30011'
def get_data(the_host='127.0.0.1:27017',
             the_db='twitter_user_tweet',
             the_col='user',
             screen_name_list=list()):
    """
    根据推特用户screen_name列表，从数据库中查找用户的详细信息
    :param the_host: 服务器地址
    :param the_db: 数据库
    :param the_col: 集合
    :param screen_name_list: 待查找的用户screen_name列表
    :return: 查找的结果
    """

    data_col = MongoClient(the_host).get_database(the_db).get_collection(the_col)
    search_result = []  # 存放结构的列表
    # search_fail = []    # 存放查找失败的用户

    for screen_name in screen_name_list:
        # (1)返回所有的字段
        # user_detail = data_col.find_one({'screen_name': screen_name}, {"_id": 0})
        # (2)指定返回某些字段
        user_detail = data_col.find_one({'screen_name': screen_name},
                                        {"_id": 0, "description": 1, "head_url": 1, "name": 1, "head_image": 1,
                                         "screen_name": 1})
        if user_detail:
            search_result.append(user_detail)
        else:
            search_result.append({"screen_name": screen_name})
            # search_fail.append({"screen_name": screen_name})

    # result = json.dumps({"search_result": search_result})
    result = search_result
    return result


if __name__ == "__main__":
    _result = get_data(screen_name_list=['bbccouk', 'XXXXXX'])
    print _result
