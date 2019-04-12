# -*- coding:utf-8 -*-
import sys

from pymongo import MongoClient
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

reload(sys)
sys.setdefaultencoding('utf-8')

import logging
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver import ActionChains
from random import randint
from configure import *
from search.util.config_read_util import config_set
from search.util.logger_util import log_util
from search.util.path_util import path_dir_parent
from selenium.common.exceptions import NoSuchElementException
from search.util.picture_write import linkedin_save_to_local


class LinkedinSpider(object):
    """
    设置日志文件路径
    """
    # 类变量
    path = os.path.join(path_dir_parent(__file__) + "/data/logging/LinkedIn_search.log")
    value = "('" + path + "', 'a')"
    config_set("logging.ini", "handler_hand02", "args", value)
    log_util()
    logger_name = "LinkedIn_search"
    logger = logging.getLogger(logger_name)

    def __init__(self, name):
        """
        初始化浏览器选项
        :param name:
        """
        self.chrome_options = webdriver.ChromeOptions()
        # self.chrome_options.add_argument('--headless')
        # self.chrome_options.add_argument('--disable-gpu')
        # self.chrome_options.add_argument('--no-sandbox')
        # self.chrome_options.add_argument('--proxy-server=%s' % PROXY)  # 用代理跑driver
        # 需要指定chromedriver的位置
        self.browser = webdriver.Chrome(executable_path="E://PycharmProjects//webdriver//chromedriver",
                                        chrome_options=self.chrome_options)
        # self.browser = webdriver.Chrome(chrome_options=self.chrome_options)
        self.keywords = name
        self.information_list = []

    def login(self, linkedin_account, linkedin_password):
        """
        登陆函数
        :return: 登陆结果
        """
        # 访问linkedin网页
        self.browser.get('https://www.linkedin.com/')
        WebDriverWait(self.browser, 60).until(expected_conditions.presence_of_element_located(
            (By.CLASS_NAME, "login-form")))
        # 输入账户密码
        self.browser.find_element_by_name('session_key').clear()
        self.browser.find_element_by_name('session_key').send_keys(linkedin_account)
        time.sleep(2)
        self.browser.find_element_by_name('session_password').clear()
        self.browser.find_element_by_name('session_password').send_keys(linkedin_password)
        time.sleep(2)
        # 模拟点击登录按钮，两种不同的点击方法。。。
        try:
            self.browser.find_element_by_id('login-submit').send_keys(Keys.ENTER)
            time.sleep(3)
        except:
            error = linkedin_account, "login error!"
            print error
            # self.logger.info(error)
            return False

        success = linkedin_account, "login success!"
        print success
        # self.logger.info(success)
        return True

    def search(self):
        """
        跳转到搜索界面
        :return: 用户名 个人主页 用户信息
        """
        try:
            for i in range(1, 2):
                i = str(i)
                url = "https://www.linkedin.com/search/results/all/?keywords=" + self.keywords + "&page=" + i
                time.sleep(3)
                self.browser.get(url)
                self.find_user()
        except Exception, e:
            error = "error:", e.message
            # self.logger.info(error)
            print error
        self.logger.info("crawler success")
        print "crawler success"
        return self.information_list

    def find_user(self):
        """
        解析函数 找出用户名 个人主页 个人信息
        :return: 个人信息
        """
        lis = self.browser.find_elements_by_class_name("search-result__occluded-item")
        self.page_down()
        for li in lis:
            information = {}
            # 主页链接
            try:
                tag = li.find_element_by_tag_name("a")
                href = tag.get_attribute("href")
                information["person_website"] = href
                print href
            except NoSuchElementException:
                information["person_website"] = None
                pass
            # 用户名
            try:
                span_name = li.find_element_by_css_selector(".name.actor-name")  # class之间的空格 表示是复合类 可以用这种方式查找
                name = span_name.text
                information["name"] = name
                print name
            except NoSuchElementException:
                information["name"] = None
                pass
            # 职业头衔
            try:
                span_title = li.find_element_by_css_selector(
                    ".subline-level-1.t-14.t-black.t-normal.search-result__truncate")  # class之间的空格 表示是复合类 可以用这种方式查找
                title = span_title.text
                information["title"] = title
                print title
            except NoSuchElementException:
                information["title"] = None
                pass
            # 地理位置
            try:
                span_company_location = li.find_element_by_css_selector(
                    ".subline-level-2.t-12.t-black--light.t-normal.search-result__truncate")
                company_location = span_company_location.text
                information["company_location"] = company_location
                print company_location
            except NoSuchElementException:
                information["company_location"] = None
                pass
            # 描述信息
            try:
                span_background_summary = li.find_element_by_css_selector(
                    ".search-result__snippets.mt2.t-12.t-black--light.t-normal")
                background_summary = span_background_summary.text
                information["background_summary"] = background_summary
                print background_summary
            except NoSuchElementException:
                information["background_summary"] = None
                pass
            # 头像链接
            try:
                span_head_url = li.find_element_by_css_selector(
                    ".lazy-image.ivm-view-attr__img--centered.EntityPhoto-circle-4.presence-entity__image.EntityPhoto-circle-4.loaded")
                head_url = span_head_url.get_attribute("src")
                information["head_url"] = head_url
                print head_url
            except NoSuchElementException:
                information["head_url"] = None
                pass
            self.logger.info(information)
            self.information_list.append(information)

    def page_down(self):
        """
        下拉函数
        :return:
        """
        # ActionChains(self.driver).send_keys(Keys.DOWN).perform()
        ActionChains(self.browser).send_keys(Keys.END).perform()  # 拉到底
        wait = randint(3, 5)
        time.sleep(wait)

    def main(self, linkedin_account, linkedin_password):
        """
        主运行函数
        :return: 搜索结果
        """
        login = self.login(linkedin_account, linkedin_password)
        if login:
            search = self.search()
            self.browser.quit()
            return search


# 链接领英用户信息数据库
class linkedinClient(object):
    def __init__(self, linkedin_host, linkedin_database, linkedin_collection):
        self.client = MongoClient(linkedin_host)
        self.database = self.client.get_database(linkedin_database)
        self.collection = self.database.get_collection(linkedin_collection)
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
                    try:
                        head_image = linkedin_save_to_local(image_url)
                        item["head_image"] = head_image
                    except Exception:
                        item["head_image"] = None
                        pass
                else:
                    item["head_image"] = None
                self.update_data("person_website", item["person_website"], item)
            flag = True
        except Exception, e:
            flag = False
            pass
        return flag


# 链接领英账户数据库
class Account(object):
    def __init__(self):
        self.client = MongoClient(userHost)
        self.database = self.client.get_database(userDatabase)
        self.collection = self.database.get_collection(userCollection)

    def get_account(self):
        """
        获取领英账户用户名 密码
        :return: 用户名 密码
        """
        account = self.collection.find({}).skip(randint(0, 600)).limit(1)[0]
        return account['account'], account['password']


if __name__ == '__main__':
    pass
