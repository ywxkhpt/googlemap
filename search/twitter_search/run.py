# -*- coding:utf-8 -*-
# 功能：在推特搜索栏输入相应的内容“A”，抓取和“A”想关的用户信息
from API import API, Account, TweetsClient
from configure import *
from get_twitter_data import get_data


def run(name):
    """
    爬取搜索主函数
    :param name: 搜索的人名
    :return: 爬取的结果
    """
    # 待搜索内容
    KEYWORDS = name

    # 获取账号
    twitter_account = Account()
    t_account = twitter_account.get_account()
    # 登陆账号采集
    Crawler = API(proxy=PROXY, keywords=KEYWORDS)
    result = Crawler.crawler(twitter_account="hptuestc@gmail.com",
                             twitter_password="he19910824", host=tweet_host, database=tweet_database,
                             collection=tweet_collection)
    # return Crawler.crawler(twitter_account=t_account[0],
    #                        twitter_password=t_account[1])
    # 将信息存储到数据库
    client = TweetsClient(tweet_host, tweet_database, tweet_collection)
    flag = client.save_to_database(result)
    if flag is True:
        print "插入成功"
        person_website_list = list()
        for item in result:
            person_website = item["screen_name"]
            person_website_list.append(person_website)
        print person_website_list
        data = get_data(screen_name_list=person_website_list)
        return data
    else:
        print "插入失败"
        return None


if __name__ == "__main__":
    result = run('allen')
    print result
