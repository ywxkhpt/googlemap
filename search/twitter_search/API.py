# -*- coding:utf-8 -*-
# 功能：twitter用户搜索
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from selenium import webdriver
import time
from configure import *
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from random import randint
from search.util.config_read_util import config_read, config_set
from search.util.path_util import path_dir_parent
from pymongo import MongoClient
from search.util.logger_util import log_util
import logging
import os
from search.util.picture_write import twitter_save_to_local


class API(object):
    """
    设置日志文件的路径
    """
    # 类变量
    path = os.path.join(path_dir_parent(__file__) + "/data/logging/twitter_search.log")
    value = "('" + path + "', 'a')"
    config_set("logging.ini", "handler_hand01", "args", value)
    log_util()
    logger_name = "twitter_search"
    logger = logging.getLogger(logger_name)

    # 对象变量
    def __init__(self, proxy, keywords):
        """
        初始化浏览器选项
        :param proxy: 代理
        :param keywords: 搜索关键词
        """
        self.chrome_options = webdriver.ChromeOptions()
        # 设置无界面浏览器
        # 服务器端需要设置无头
        # self.chrome_options.add_argument('--headless')
        # self.chrome_options.add_argument('--disable-gpu')
        # self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--proxy-server=%s' % proxy)  # 用代理跑driver
        # 需要指定chromedriver的位置
        self.driver = webdriver.Chrome(executable_path="E://PycharmProjects//webdriver//chromedriver",
                                        chrome_options=self.chrome_options)
        # self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
        self.keywords = keywords

    def login(self, email, pass_word):
        """
        登录函数
        :param email:用户名
        :param pass_word:密码
        :return:登陆成功返回true
        """
        login_url = 'https://twitter.com/login/'
        while True:
            self.driver.get(login_url)
            try:
                WebDriverWait(self.driver, 180).until(expect.presence_of_element_located(
                    (By.CLASS_NAME, "js-username-field")))
                print "tying to login now......"
                self.driver.find_element_by_class_name('js-username-field').send_keys(email)
                time.sleep(3)
                self.driver.find_element_by_class_name('js-password-field').send_keys(pass_word)
                time.sleep(3)
                self.driver.find_element_by_css_selector('button.submit').click()
                WebDriverWait(self.driver, 60).until(expect.presence_of_element_located
                                                     ((By.CLASS_NAME, "topbar-tweet-btn")))
                print email, "login success!"
                return True
            except NoSuchElementException:
                print email, "login fail!(Can't find expect elements)"
                self.driver.refresh()
                time.sleep(3)
                continue
            except TimeoutException:
                print email, "login fail for time out!"
                time.sleep(3)
                continue

    def search(self):
        """
        搜索函数 转到搜索页面
        :return: 成功返回true
        """
        self.driver.get("https://twitter.com/search?f=users&vertical=news&q=" + self.keywords + "&src=typd")
        # self.driver.find_element_by_class_name('search-input').send_keys(self.keywords)
        # self.driver.find_element_by_class_name('search-icon').click()
        try:
            WebDriverWait(self.driver, 60).until(expect.presence_of_element_located
                                                 ((By.CLASS_NAME, 'SearchNavigation-titleText')))
            flag = True
        except NoSuchElementException:
            flag = False
        return flag

    def parse(self):
        """
        解析搜索结果
        :return: 用户名和个人主页的列表
        """
        information_list = []  # 返回信息
        try:
            count = 10
            times = 5
            while True:
                tags = self.driver.find_elements_by_class_name('ProfileCard-content')  # 获取当前显示的用户（逐条）
                if count <= len(tags):
                    break
                if times <= 0:
                    break
                # count = len(tags)
                self.page_down()
                times = times - 1
            print time.ctime(), "开始采集新的网页......."
            tags = self.driver.find_elements_by_class_name('ProfileCard-content')  # 获取当前显示的用户（逐条）
            count = len(tags)
            print time.ctime(), 'len_tags:', count
            # 获取每一条的详细信息
            for num in range(0, count):
                div = tags[num]
                user_dic = {}
                # 采集头像链接
                try:
                    span_head_url = div.find_element_by_css_selector(
                        ".ProfileCard-avatarImage.js-action-profile-avatar")
                    head_url = span_head_url.get_attribute("src")
                    print head_url
                    user_dic["head_url"] = head_url
                except NoSuchElementException:
                    user_dic["head_url"] = None
                    pass
                # 用户的个人主页 用户的name
                try:
                    span_person_website = div.find_element_by_css_selector(
                        ".fullname.ProfileNameTruncated-link.u-textInheritColor.js-nav")
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
                # 描述信息
                try:
                    span_description = div.find_element_by_css_selector(
                        ".ProfileCard-bio.u-dir")
                    description = span_description.text
                    print description
                    user_dic["description"] = description
                except NoSuchElementException:
                    user_dic["description"] = None
                    pass
                # 用户的screen_name
                try:
                    span_screen_name = div.find_element_by_class_name(
                        "u-linkComplex-target")
                    screen_name = span_screen_name.text
                    print screen_name
                    user_dic["screen_name"] = screen_name
                except NoSuchElementException:
                    user_dic["screen_name"] = None
                    pass
                # 用户信息
                information_list.append(user_dic)
                self.logger.info("个人信息采集完成")

        except Exception as Err:
            print Err.message, "error......"
        return information_list

    def page_down(self):
        """
        下拉函数
        :return:
        """
        for i in range(3):
            # ActionChains(self.driver).send_keys(Keys.DOWN).perform()
            ActionChains(self.driver).send_keys(Keys.END).perform()  # 拉到底
            wait = randint(3, 10)
            time.sleep(wait)

    def crawler(self, twitter_account, twitter_password, host=None, database=None, collection=None):
        page = self.login(twitter_account, twitter_password)  # 尝试登录，登录成功则继续执行
        if page:
            self.search()
            result = self.parse()
            # self.logger.info("crawler success")
            print "crawler success"
            try:
                self.driver.quit()
            except Exception:
                pass
            return result
        else:
            # self.logger.info("login error")
            try:
                self.driver.quit()
            except Exception:
                pass
            print "login error"



# 链接推特用户信息数据库
class TweetsClient(object):
    def __init__(self, tweet_host, tweet_database, tweet_collection):
        self.client = MongoClient(tweet_host)
        self.database = self.client.get_database(tweet_database)
        self.collection = self.database.get_collection(tweet_collection)
        self.create_unique_index()

    def create_unique_index(self):
        self.collection.ensure_index([("person_website", 1)], unique=True)

    def update_data(self, key_str, key, data):  # 根据唯一标示key，更新数据库的内容
        self.collection.update({key_str: key}, {'$set': data}, upsert=True)

    def save_to_database(self, result):
        """
        用户信息存储到数据库
        :return: 插入是否成功
        """
        try:
            # 存储头像图片
            # 存储用户信息 person_website
            # 应该要建立索引
            for item in result:
                # print item["person_website"]
                if item["person_website"] is None:
                    continue
                image_url = item["head_url"]
                if image_url is not None:
                    # print image_url
                    try:
                        head_image = twitter_save_to_local(image_url)
                        item["head_image"] = head_image
                    except Exception:
                        item["head_image"] = None
                        pass
                else:
                    item["head_image"] = None
                self.update_data("person_website", item["person_website"], item)
            flag = True
        except Exception, e:
            print "下载图片出错"
            flag = False
            pass
        return flag


# 链接推特账户数据库
class Account(object):
    def __init__(self):
        self.client = MongoClient(userHost)
        self.database = self.client.get_database(userDatabase)
        self.collection = self.database.get_collection(userCollection)

    def get_account(self):
        account = self.collection.find({}).skip(randint(0, 70)).limit(1)[0]
        return account['account'], account['pwd']
