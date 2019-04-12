# -*- coding:utf-8 -*-

from LinkedInSpider import LinkedinSpider, Account,linkedinClient
from configure import *
from get_linked_data import get_data


def run(name):
    """
    运行主函数
    :param name: 搜索的人名
    :return: 用户信息
    """
    # 待搜索内容
    KEYWORDS = name

    # 获取账号
    twitter_account = Account()
    l_account = twitter_account.get_account()
    # 登陆账号采集
    spider = LinkedinSpider(name=KEYWORDS)
    # spider.main(linkedin_account=l_account[0],
    #             linkedin_password=l_account[1])
    result = spider.main(linkedin_account=account,
                       linkedin_password=password)
    # 将信息存储到数据库
    client = linkedinClient(linkedin_host, linkedin_database, linkedin_collection)
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


if __name__ == '__main__':
    website_list = run("allen")
    print website_list
