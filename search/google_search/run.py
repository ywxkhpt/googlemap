# -*- coding:utf-8 -*-
# facebook爬虫

from GoogleSpider import *
from configure import *
from get_google_data import get_data

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
    spider = GoogleSpider(proxy=PROXY, keywords=KEYWORDS)
    # return spider.main(account=f_account[0],
    #                    password=f_account[1])
    result = spider.main(account=account,
                         password=password)
    # 将信息存储到数据库
    print result
    client = GoogleClient(google_host, google_database, google_collection)
    flag = client.save_to_database(result)
    if flag is True:
        print "插入成功"
        person_website_list = list()
        for item in result:
            person_website = item["webpage_url"]
            person_website_list.append(person_website)
        website_list = person_website_list
        return get_data(webpage_urls=website_list)
    else:
        print "插入失败"
        return None


if __name__ == "__main__":
    result = run('allen')
    print result