# -*- coding:utf-8 -*-
from pymongo import MongoClient
import json

# the_host='mongodb://liuchang:liuchang314@121.49.99.14:30011'
def get_data(the_host='mongodb://127.0.0.1:27017',
             the_db='google',
             the_col='search_result',
             webpage_urls=list()):
    """
    根据领英用户链接列表，从数据库中查找用户的详细信息
    :param the_host: 服务器地址
    :param the_db: 数据库
    :param the_col: 集合
    :param webpage_urls: 搜索结果的链接列表
    :return: 查找的结果
    """

    data_col = MongoClient(the_host).get_database(the_db).get_collection(the_col)
    search_result = []  # 存放结构的列表

    for url in webpage_urls:
        # user_detail = data_col.find_one({'person_website': url}, {"_id": 0})
        # 可指定输出某些字段
        user_detail = data_col.find_one({'webpage_url': url},
                                        {"_id": 0, "webpage_url": 1, "webpage_title": 1, "webpage_description": 1})
        if user_detail:
            search_result.append(user_detail)
        else:
            search_result.append({"webpage_url": url})
            # search_fail.append({"person_website": url})

    # result = json.dumps({"search_result": search_result})  # 转化为json格式
    result = search_result  # 转化为json格式
    return result


if __name__ == "__main__":
    _result = get_data(webpage_urls=['', ''])
    print _result
