# -*- coding:utf-8 -*-

import sys

from pymongo import MongoClient

reload(sys)
sys.setdefaultencoding('utf-8')

import logging
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver import ActionChains
from random import randint
from selenium.webdriver.support.wait import WebDriverWait
from configure import *
from search.util.config_read_util import config_set
from search.util.logger_util import log_util
from search.util.path_util import path_dir_parent
from selenium.webdriver.support import expected_conditions


class GoogleSpider(object):
    """
    设置日志文件
    """
    # 类变量
    path = os.path.join(path_dir_parent(__file__) + "/data/logging/google_search.log")
    value = "('" + path + "', 'a')"
    config_set("logging.ini", "handler_hand04", "args", value)
    log_util()
    logger_name = "google_search"
    logger = logging.getLogger(logger_name)

    def __init__(self, proxy, keywords):
        """
        初始化浏览器选项
        :param proxy: 代理
        :param keywords: 搜索关键词
        """
        self.chrome_options = webdriver.ChromeOptions()
        # 不弹出通知
        prefs = {
            'profile.default_content_setting_values':
                {
                    'notifications': 2
                }
        }
        # self.chrome_options.add_argument('--headless')
        # self.chrome_options.add_argument('--disable-gpu')
        # self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_experimental_option('prefs', prefs)
        self.chrome_options.add_argument('--proxy-server=%s' % proxy)  # 用代理跑driver
        # 需要指定chromedriver的位置
        self.browser = webdriver.Chrome(executable_path="E://PycharmProjects//webdriver//chromedriver",
                                        chrome_options=self.chrome_options)
        # self.browser = webdriver.Chrome(chrome_options=self.chrome_options)
        self.keywords = keywords

    def search(self):
        """
        跳转到搜索界面
        :return: 搜索是否成功
        """
        url = "https://www.google.com/"
        self.browser.get(url)
        time.sleep(3)
        try:
            self.browser.find_element_by_css_selector(".gLFyf.gsfi")
            url = "https://www.google.com/search?q=" + self.keywords + "&btnG=Search&safe=strict&h1=en&gbv=1&num=10"
            self.browser.get(url)
            time.sleep(5)
            print "open search_page success"
            flag = True
        except NoSuchElementException:
            flag = False
            print "open search_page fail"
            # self.logger.info("search fail")

        return flag

    def page_down(self):
        """
        下拉函数
        :return:
        """
        ActionChains(self.browser).send_keys(Keys.END).perform()  # 拉到底
        wait = randint(3, 6)
        time.sleep(wait)

    def find_user(self):
        """
        解析函数
        :return: 网页描述信息 网页链接
        """
        self.page_down()
        time.sleep(2)
        information_list = []  # 返回信息
        print time.ctime(), "开始采集新的用户......."
        try:
            div_search = self.browser.find_element_by_id('search')  # 获取当前显示的用户（逐条）
            div_ires = div_search.find_element_by_id("ires")
            div_rso = div_ires.find_element_by_id("rso")
            div_g = div_rso.find_elements_by_class_name("g")
            for g in div_g:
                information = {}
                div_rc = g.find_element_by_class_name("rc")
                # 网页标题
                try:
                    div_LC20lb = div_rc.find_element_by_class_name("LC20lb")
                    webpage_title =  div_LC20lb.text
                    information["webpage_title"] = webpage_title
                    print webpage_title
                except NoSuchElementException:
                    information["webpage_title"] = None
                    pass
                # 网页链接
                try:
                    div_iUh30 = div_rc.find_element_by_class_name("iUh30")
                    webpage_url = div_iUh30.text
                    information["webpage_url"] = webpage_url
                    print webpage_url
                except NoSuchElementException:
                    information["webpage_url"] = None
                    pass
                # 网页描述
                try:
                    div_s = div_rc.find_element_by_class_name("s")
                    webpage_description = div_s.text
                    information["webpage_description"] = webpage_description
                    print webpage_description
                except NoSuchElementException:
                    information["webpage_description"] = None
                    pass
                # print "网页采集完毕"
                self.logger.info("网页采集完毕")
                information_list.append(information)
        except Exception:
            self.logger.info("crawler error...")
        self.logger.info("crawler success")
        print "crawler success"
        return information_list

    def main(self, account, password):
        """
        运行主函数
        :param account: 账户名
        :param password: 密码
        :return: 爬取的搜索结果
        """
        search = self.search()
        if search:
            search_result = self.find_user()
            self.browser.quit()
            return search_result


# 链接google信息数据库
class GoogleClient(object):
    def __init__(self, google_host, google_database, google_collection):
        self.client = MongoClient(google_host)
        self.database = self.client.get_database(google_database)
        self.collection = self.database.get_collection(google_collection)
        self.create_unique_index()

    def create_unique_index(self):
        self.collection.ensure_index([("webpage_url", 1)], unique=True)

    def update_data(self, key_str, value, data):  # 根据唯一标示key，更新数据库的内容
        self.collection.update({key_str: value}, {'$set': data}, upsert=True)

    def save_to_database(self, result):
        """
        用户信息存储到数据库
        :return: 插入是否成功
        """
        try:
            # 存储网页信息
            # 应该要建立索引
            for item in result:
                # print item["person_website"]
                if item["webpage_url"] is None:
                    continue
                self.update_data("webpage_url", item["webpage_url"], item)
            flag = True
        except Exception, e:
            flag = False
            pass
        return flag


# 链接facebook账户数据库
class Account(object):
    def __init__(self):
        self.client = MongoClient(userHost)
        self.database = self.client.get_database(userDatabase)
        self.collection = self.database.get_collection(userCollection)

    def get_account(self):
        """
        获取facebook账户用户名 密码
        :return: 用户名 密码
        """
        account = self.collection.find({}).skip(randint(0, 70)).limit(1)[0]
        return account['account'], account['pwd']


if __name__ == '__main__':
    pass
