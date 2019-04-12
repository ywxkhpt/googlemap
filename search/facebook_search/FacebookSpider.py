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
from search.util.picture_write import facebook_save_to_local, save_to_local


class FacebookSpider(object):
    """
    设置日志文件
    """
    # 类变量
    path = os.path.join(path_dir_parent(__file__) + "/data/logging/facebook_search.log")
    value = "('" + path + "', 'a')"
    config_set("logging.ini", "handler_hand03", "args", value)
    log_util()
    logger_name = "facebook_search"
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

    def login(self, email, password):
        """
        登陆函数
        :param email: 邮箱
        :param password: 密码
        :return: 登陆结果
        """
        # 访问facebook网页
        self.browser.get('https://www.facebook.com/')
        WebDriverWait(self.browser, 60).until(expected_conditions.presence_of_element_located(
            (By.ID, "login_form")))
        # 输入账户密码
        self.browser.find_element_by_id('email').clear()
        self.browser.find_element_by_id('email').send_keys(email)
        time.sleep(2)
        self.browser.find_element_by_id('pass').clear()
        self.browser.find_element_by_id('pass').send_keys(password)
        time.sleep(2)
        # 模拟点击登录按钮，两种不同的点击方法。。。
        try:
            self.browser.find_element_by_id('loginbutton').send_keys(Keys.ENTER)
            time.sleep(3)
        except Exception, e:
            print e.message
            error = email, "login error!"
            print error
            # self.logger.info(error)
            return False

        success = email, "login success!"
        print success
        # self.logger.info(success)
        return True

    def search(self):
        """
        跳转到搜索界面
        :return: 搜索是否成功
        """
        url = "https://www.facebook.com/search/people/?q=" + self.keywords + "&epa=SERP_TAB"
        self.browser.get(url)
        try:
            WebDriverWait(self.browser, 60).until(expected_conditions.presence_of_element_located
                                                  ((By.ID, 'initial_browse_result')))
            flag = True
        except NoSuchElementException:
            flag = False
            print "search fail"
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
        :return: 用户名 主页链接信息
        """
        information_list = []  # 返回信息
        try:
            count = 10
            times = 5
            while True:
                tags = self.browser.find_elements_by_class_name('_4p2o')  # 获取当前显示的用户（逐条）
                if count <= len(tags):
                    break
                if times <= 0:
                    break
                count = len(tags)
                self.page_down()
                times = times - 1
            print time.ctime(), "开始采集新的用户......."
            tags = self.browser.find_elements_by_class_name('_4p2o')  # 获取当前显示的用户（逐条）
            count = len(tags)
            print time.ctime(), 'len_tags:', count
            # 获取每一条的详细信息
            for num in range(0, count):
                div = tags[num]
                user_dic = {}
                # 头像链接
                try:
                    span_head_url = div.find_element_by_css_selector("._1glk._6phc.img")
                    head_url = span_head_url.get_attribute("src")
                    print head_url
                    user_dic["head_url"] = head_url
                except NoSuchElementException:
                    user_dic["head_url"] = None
                    pass
                # _32mo
                # 用户的个人主页 用户名
                try:
                    span_person_website = div.find_element_by_class_name("_32mo")
                    person_website = span_person_website.get_attribute("href")
                    name = span_person_website.text
                    print person_website
                    print name
                    user_dic["person_website"] = person_website
                    user_dic["name"] = name
                except NoSuchElementException:
                    user_dic["person_website"] = None
                    user_dic["name"] = None
                    pass
                # 地理位置
                try:
                    span_location = div.find_element_by_class_name("_pac")
                    location = span_location.text
                    print location
                    user_dic["location"] = location
                except NoSuchElementException:
                    user_dic["location"] = None
                    pass
                # 描述信息
                try:
                    span__glo = div.find_element_by_class_name("_glo")
                    span__ajw = span__glo.find_elements_by_class_name("_ajw")
                    description = ""
                    for _ajw in span__ajw:
                        _52eh = _ajw.find_element_by_class_name("_52eh")
                        # print _52eh.text
                        description = description + _52eh.text + "\n"
                    print description
                    user_dic["description"] = description
                except NoSuchElementException:
                    user_dic["description"] = None
                    pass
                information_list.append(user_dic)
                print "个人信息采集完毕"
                self.logger.info("个人信息采集完毕")
        except Exception as Err:
            error = "error:", Err.message
            print error
            # self.logger.info(error)
        # self.logger.info("crawler success")
        print "crawler success"
        return information_list

    def main(self, account, password):
        """
        运行主函数
        :param account: 账户名
        :param password: 密码
        :return: 爬取的搜索结果
        """
        login = self.login(account, password)
        if login:
            search = self.search()
            if search:
                user_information = self.find_user()
                self.browser.quit()
                return user_information


            # 链接facebook用户信息数据库
class facebookClient(object):
    def __init__(self, facebook_host, facebook_database, facebook_collection):
        self.client = MongoClient(facebook_host)
        self.database = self.client.get_database(facebook_database)
        self.collection = self.database.get_collection(facebook_collection)
        self.create_unique_index()

    def create_unique_index(self):
        self.collection.ensure_index([("person_website", 1)], unique=True)

    def update_data(self, key_str, value, data):  # 根据唯一标示key，更新数据库的内容
        self.collection.update({key_str: value}, {'$set': data}, upsert=True)

    def save_to_database(self, result):
        """
        用户信息存储到数据库
        :return: 插入是否成功
        """
        # 存储头像图片
        # 存储用户信息 person_website
        # 应该要建立索引
        try:
            for item in result:
                # print item["person_website"]
                if item["person_website"] is None:
                    continue
                image_url = item["head_url"]
                if image_url is not None:
                    try:
                        head_image = facebook_save_to_local(image_url)
                        item["head_image"] = head_image
                    except Exception:
                        item["head_image"] = None
                else:
                    item["head_image"] = None
                self.update_data("person_website", item["person_website"], item)
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
