# -*- coding:utf-8 -*-
# facebook爬虫

from FacebookSpider import *
from configure import *
from get_facebook_data import get_data


def run(name):
    """
    运行主函数
    :param name: 用户名
    :return: 搜索结果
    """
    # 待搜索内容
    KEYWORDS = name

    # 获取账号
    facebook_account = Account()
    f_account = facebook_account.get_account()
    # 登陆账号采集
    spider = FacebookSpider(proxy=PROXY, keywords=KEYWORDS)
    # return spider.main(account=f_account[0],
    #                    password=f_account[1])
    result = spider.main(account=account,
                         password=password)
    # 将信息存储到数据库
    client = facebookClient(facebook_host, facebook_database, facebook_collection)
    flag = client.save_to_database(result)
    if flag is True:
        print "插入成功"
        person_website_list = list()
        for item in result:
            person_website = item["person_website"]
            person_website_list.append(person_website)
        data = get_data(person_websites=person_website_list)
        return data
    else:
        print "插入失败"
        return None


if __name__ == "__main__":
    result = run('allen')
    print result
