# -*- coding:utf-8 -*-
from pymongo import MongoClient
import json


# the_host='mongodb://liuchang:liuchang314@121.49.99.14:30011'
def get_data(the_host='mongodb://127.0.0.1:27017',
             the_db='LinkedIn',
             the_col='user_information',
             person_websites=list()):
    """
    根据领英用户链接列表，从数据库中查找用户的详细信息
    :param the_host: 服务器地址
    :param the_db: 数据库
    :param the_col: 集合
    :param person_websites: 待查找的用户主链接列表
    :return: 查找的结果
    """

    data_col = MongoClient(the_host).get_database(the_db).get_collection(the_col)
    search_result = []  # 存放结构的列表
    # search_fail = []    # 存放查找失败的用户

    for url in person_websites:
        # user_detail = data_col.find_one({'person_website': url}, {"_id": 0})
        # 可指定输出某些字段
        user_detail = data_col.find_one({'person_website': url},
                                        {"_id": 0, "person_website": 1, "name": 1, "title": 1, "head_url": 1,
                                         "company_location": 1, "background_summary": 1, "head_image": 1})
        if user_detail:
            search_result.append(user_detail)
        else:
            search_result.append({"person_website": url})
            # search_fail.append({"person_website": url})

    # result = json.dumps({"search_result": search_result})  # 转化为json格式
    # result = json.dumps(search_result)  # 转化为json格式
    result = search_result  # 转化为json格式
    return result


if __name__ == "__main__":
    _result = get_data(person_websites=['https://ch.linkedin.com/in/cezarmaroti/zh-cn', 'https://cuowu/'])
    print _result
