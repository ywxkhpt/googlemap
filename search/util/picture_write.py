# -*- coding:utf-8 -*-
"""
将图片存储到本地 并返回图片的路径
"""
import requests
import uuid

save_dir = "E:\pictures"


def save_to_local(image_url):
    """
    文件存储到本地
    :param image_url: 图片地址
    :return: 图片存储路径
    """
    image = requests.get(image_url)
    file_name = save_dir + "\\" + str(uuid.uuid1()).replace('-', '') + '.jpg'
    with open("%s" % file_name, 'wb') as file:
        file.write(image.content)
    return file_name


def facebook_save_to_local(image_url):
    """
    文件存储到本地
    :param image_url: 图片地址
    :return: 图片存储路径
    """
    proxies = {'http': 'http://kb111.asuscomm.com:8118', 'https': 'https://kb111.asuscomm.com:8118'}
    image = requests.get(image_url, proxies=proxies, verify=False)
    file_name = save_dir + "\\facebook\\" + str(uuid.uuid1()).replace('-', '') + '.jpg'
    with open("%s" % file_name, 'wb') as file:
        file.write(image.content)
    return file_name


def twitter_save_to_local(image_url):
    """
    文件存储到本地
    :param image_url: 图片地址
    :return: 图片存储路径
    """
    proxies = {'http': 'http://kb111.asuscomm.com:8118', 'https': 'http://kb111.asuscomm.com:8118'}
    image = requests.get(image_url,proxies=proxies, verify=False)
    file_name = save_dir + "\\twitter\\" + str(uuid.uuid1()).replace('-', '') + '.jpg'
    with open("%s" % file_name, 'wb') as file:
        file.write(image.content)
    return file_name


def linkedin_save_to_local(image_url):
    """
    文件存储到本地
    :param image_url: 图片地址
    :return: 图片存储路径
    """
    # proxies = {'http': 'http://kb111.asuscomm.com:8118', 'https': 'http://kb111.asuscomm.com:8118'}
    image = requests.get(image_url)
    file_name = save_dir + "\\linkedin\\" + str(uuid.uuid1()).replace('-', '') + '.jpg'
    with open("%s" % file_name, 'wb') as file:
        file.write(image.content)
    return file_name


if __name__ == "__main__":
    link = "https://scontent-icn1-1.xx.fbcdn.net/v/t1.0-1/p74x74/20882841_103420570387198_2182994975060665553_n.jpg?_nc_cat=105&_nc_ht=scontent-icn1-1.xx&oh=355a0fbb4ab6885d1bc6ce98b2aa41cf&oe=5D0A787F"
    print facebook_save_to_local(link)
