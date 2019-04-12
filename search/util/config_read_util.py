#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
读取配置文件
"""

import ConfigParser
from path_util import *


def config_read(config_file_name, section, option):
    config_file_path = path_dir_parent(__file__) + "/configure/" + config_file_name
    # print config_file_path
    cf = ConfigParser.ConfigParser()
    cf.read(config_file_path)
    if option is "user_agents" or option is "domain":
        return [i.strip() for i in cf.get(section, option).split('*')]
    else:
        return cf.get(section, option)


def config_set(config_file_name, section, option, value):
    config_file_path = path_dir_parent(__file__) + "/configure/" + config_file_name
    # print config_file_path
    cf = ConfigParser.ConfigParser()
    cf.read(config_file_path)
    cf.set(section, option, value)
    with open(config_file_path, "w+") as f:
        cf.write(f)


if __name__ == "__main__":
    # file_name = "logging.ini"
    # section = "handler_hand02"
    # option = "args"
    # path = os.path.join(path_dir_parent(__file__), "/data/logging/twitternetwork.log")
    # value = "('" + path + "', 'a')"
    # config_set(file_name, section, option, value)
    pass